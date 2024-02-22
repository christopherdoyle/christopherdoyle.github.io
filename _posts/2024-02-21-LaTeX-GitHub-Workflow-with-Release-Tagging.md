---
title: "LaTeX GitHub Workflow with Release Tagging"
date: 2024-02-21
---
{% include snippets.html %}

<span class="caps">Create a GitHub workflow</span> for compiling {{ latex }} to PDF including version tagging on the commit and inside the PDF, and asset release.
See [christopherdoyle:LaTeXTemplate](https://github.com/christopherdoyle/LaTexTemplate) for a basic working example.
The end result is:

1. User merges PR into main.
2. Workflow pushes a new commit bumping the verison.
3. Workflow pushes a tag and release containing a compiled PDF, which includes the new version on the title page.

## The Code

Here is the YAML workflow:

{% highlight yaml linenos %}
{% raw %}
name: Build LaTeX document

on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  build_latex:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:

      - name: Set up Git repository
        uses: actions/checkout@v4
        with:
          ref: ${{ github.ref_name }}
          fetch-depth: '0'

      - name: Get next version
        id: get_next_version
        uses: thenativeweb/get-next-version@main
        with:
          prefix: 'v'

      - name: Show the next version
        run: |
          echo ${{ steps.get_next_version.outputs.version }}
          echo ${{ steps.get_next_version.outputs.hasNextVersion }}

      - name: Update version.tex, tag, commit, push
        if: steps.get_next_version.outputs.hasNextVersion == 'true'
        env:
          NEW_VERSION: ${{ steps.get_next_version.outputs.version }}
        shell: bash
        run: |
          old_version=$(git describe --tags --abbrev=0)
          sed -i "s/$old_version/$NEW_VERSION/" version.tex
          git config user.name "$(git log -n 1 --pretty=format:%an)"
          git config user.email "$(git log -n 1 --pretty=format:%ae)"
          git add version.tex
          git commit -m "Bump version $old_version->${{ steps.get_next_version.outputs.version }}"
          git push

      - name: Compile LaTeX document
        uses: xu-cheng/latex-action@3.1.0
        if: steps.get_next_version.outputs.hasNextVersion == 'true'
        with:
          root_file: main.tex

      - name: Create Release
        id: create_release
        uses: softprops/action-gh-release@v1
        if: steps.get_next_version.outputs.hasNextVersion == 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          name: Release ${{ steps.get_next_version.outputs.version }}
          tag_name: ${{ steps.get_next_version.outputs.version }}
          draft: false
          prerelease: false
          files: main.pdf
{% endraw %}
{% endhighlight %}

## How it work

We use the [get next version action](https://github.com/marketplace/actions/get-next-version) to interpret commit messages into major-minor-patch version bumps.
This is detailed on the linked page, but for example a commit message like "fix: typos" will lead to a _patch_ bump, say from 1.2.5 to 1.2.6.

To store the version inside the compiled document, we touch a small file called `version.tex` which is being `\input` to the main {{ latex }} document.
We need to have at least one tag already in git history for this to work, because we are reading the old version from the tag history (not from `version.tex` directly).
So when setting up the workflow, you need to push a tag first.

`main.tex` looks like:

{% highlight latex linenos %}
{% raw %}
\newcommand{\Version}{}

\makeatletter
\renewcommand{\maketitle}{%
    %...
    \Version{}
    %...
}
\makeatother

\input{version.tex}

\begin{document}
\maketitle
\end{document}
{% endraw %}
{% endhighlight %}

and the contents of `version.tex` is like:

```latex
\renewcommand\Version{v1.2.5}
```

We use a custom `\maketitle` to add `\Version` to the title page.
`\Version` could be defined and sed directly in `main.tex`, but it is safer to have a minimal separate file for this.

After sed-ing the version, the changes are committed with the prior commit's author meta, and pushed to the main branch.
So after this runs we have an extra commit:

* feat: added formula for three-body problem
* Bump version v1.2.5 -> 1.3.0

The first commit is you merging a PR; the second commit is from the workflow.
The new commit is not tagged yet.
First we build the PDF with [latex-action](https://github.com/xu-cheng/latex-action), then use [action-gh-release](https://github.com/softprops/action-gh-release) to push a tagged release that contains the PDF.

## Bonus: distribution to NextCloud (/Dropbox/etc.)

If you want to give your supervisor the latest version without adding them to your repository, you could use something like NextCloud WebDAV to push to a hosted NextCloud instance:

{% raw %}
```yaml
      - name: Upload Release Asset to NextCloud
        if: env.DO_BUMP_RELEASE == 'true'
        run: 'curl -u ${{ secrets.NEXTCLOUD_USERNAME }}:${{ secrets.NEXTCLOUD_PASSWORD }} -T ./main.pdf ${{ secrets.NEXTCLOUD_URL }}'
```
{% endraw %}

This requires you to set the secrets in your repository's [secrets and variables](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) page.
