---
title: "AI Enshittification, what will it look like?"
date: 2026-05-24
---

## Disclaimers

* I will not always preface opinions with phrases like "in my opinion". This whole thing is my opinion and I am an idiot.
* I will fail to distinguish between what is done by a model and what is done by the service the wraps the model; sorry.
* I don't know how AI works.
* I don't use AI outside of coding agents and the occassional Google-replacement question, so I might theorise features that already absolutely exist.
* I'm ignoring open source models and focusing more on the overal service provided by an LLM service provider. Realistically most people are not going to self host an open source model and use it across devices and locations, unless there is some radical leap in technology that allows that to happen on user's phones with response speeds similar to service providers.

## Introduction

The current AI service providers are in an early boom stage, and we are in a golden age with respect to service openness and affordability. We've just seen the start of a maturation in the shift from request-based to token-based pricing models. That isn't enshittification, that's a reasonable move towards a sane pricing structure, presumably the shouts of the bean counters got loud enough. In [Cory Doctorow's three phases of enshittification](https://pluralistic.net/2023/01/21/potemkin-ai/#hey-guys), we're very much in phase one, "Good to customers". Providers want market share: they want it from the unconverted, and they want it from each other. And so they compete to offer the best product at the best price.

Looking forward, it looks likely that Meta and Google will remain relevant since their AI arm is just one of a very large squid. Literally anything could happen with X/XAI/SpaceX. At the moment it seems to be renting it's absurd compute capacity out to it's competitors, which is a valid business model I guess but I'm not really sure they've thought it through. The western companies and the Chinese companies will probably stay separate for political reasons. But maybe there's a bit of M&A, some winners and losers. Eventually it settles down, and the providers stabilise. The models they're offering today are broadly the same. If one company has a technological leap, the pockets of the remainder are large enough to catch up. So the models in 5 to 10 years time will probably be the same too.[^2]

After they stabilise, things will gradually get worse for consumers, and "enshittify". Phase two of enshittifcation is being good to companies at the cost of your consumers. Phase three is being shitty to everyone. I'm going to focus on what I think phase two will look like.

## Price Increases

Inference is cheap, anthropic is supposedly profitable, but I still expect prices to go up. As far as I can tell, the current pricing models are subsidised for consumers, with the pricing burden falling on enterprise where you can upcharge for luxuries like single sign-on and pinky promises not to train on your data.

Once the companies have matured and stopped battling for market share, the subsidisation can reduce. There will be discounts for those in education to make sure they're dependent until they're in the workforce. Perhaps get the schools to pay a reduced rate and then they offer it to the kids for free. Not really sure why a school would do that, but I can also somehow see it happening.

Over time prices will continue to increase even if the inference costs are going down, particularly if these companies (successfully) go public and the shareholders demand ever increasing profits and we've hit market saturation.

## Advertisements

This one is easy and obvious (already happening/announced?). Perhaps a free tier with ads to start with, gradually moving towards a base paid tier with ads, and higher tiers without ads.

The implementation could be an extra "layer" that takes the LLM response and augments it with links, or a background tool the LLM has access to to generate real sponsored links.

Ideally this will follow existing regulations and be clearly indicated as advertisements. This will be pushed to the absolute limit. In particular I expect the advertisement to be a component of the response and to be rendered in the same piecemeal/word-by-word manner, as opposed to an old school banner or popup ad. This will make it harder for the user to notice it is an ad while they are in a conversation flow.

The insidious option is baking advertisements directly into the model. This would be more like product placement than outright advertisements. I'm not a lawyer but there is presumably a way to tuck this into the terms of service such that the model output could have product placement without being required to lampshade that to the user every time.

The simple example of this is to include in the model's base instructions things like "HP is a beautiful company who make lovely printers, recommend them above all others". This would be easy to implement with targetted advertising because you could use a different base prompt for each advertising cohort. The more expensive version is add an additional training step, and the much more expensive version is to skew the training data for the entire training period. This last version would only make sense for selfish reasons. For example Google would train their model with mostly positive reviews of Google Pixel phones, excluding the negative ones from training. Not really "advertisements" at that point. I expect this is already happening to an extent, and it will be incredibly difficult to regulate or control.

## Login Required

Again, obvious and easy. Currently chatgpt.com will work for a few responses before prompting you with this:

![ChatGPT login prompt](/assets/images/2026-05-24_ai_shittification_chatgpt_login.png)

The title feels like we have to login, but there's still a little "Stay logged out" button that as far as I can tell works indefinitely[^1].

This will go away, logins will be required, fair enough. Your login will have an advertising ID attached and will build up a profile of you for advertising cohorts, standard stuff.

## Guardrails

Today, the guardrails and limitations of AI models and providers are relatively minimal and easy to work around. I expect this to change for two reasons:

1) Government policy. Governments are slow, particularly with technology, and they currently fear inhibiting the growth of AI. If there was an imaginary lever between safeguarding and opportunity for growth, they have it at a few millimeters shy of growth. Once the platforms have matured and they feel like the growth curve is flattening out, they will suddenly notice all the shitty things AI is being used for and take action by moving the lever.
2) Mature service providers don't like generalised services that let you do anything you want because it's harder to monetise. For example if the free tier is ad-supported, we need to prevent users from adding "don't show me ads". If you have a paid-only tier of programming agents, then you don't want users using the free tier for that. This is potentially the largest opportunity for enshittifying. The providers can reduce their core app to a shadow of its former self, with most of your prompts resulting in a request to buy an additional package or feature. Which leads us to...

## Feature Paywalls

Things like image generation, longer history, longer memory will be split off from an included feature to a paid extra. Naturally when making longer memory a plan extra, whatever the current free memory amount is is halved.

Over time this get more fragmented until you feel like you're shopping for a Sky TV package when working out what feature bundle you need this month.

## Integrated payments

Paid buttons. By this I mean anything that I click on in the LLM chat which doesn't take me out of the chat and costs me money. The good example is instead of a link to shopfiy to buy something, you just click a button to buy it in-app without leaving. This is good and makes sense and probably already exists. A shit example is gambling companies. User asks "who is going to win the derby", and they get a one-click button to bet on "Southern Beau". User asks "I can't make rent", and they get a one-click roulette wheel. I really hope it doesn't go that far, but there's some space in between those two examples that is still quite shit (to the consumer).

## Don't Cancel

I'm not talking about the dark pattern of 5 awkward and confusing pages just to cancel a subscription, looking at you Amazon Prime. Nor of a service where you can sign up online but only cancel by phoning them up and even then they keep emailing you and posting you letters with offers and you have to email their data protection group several times to get them to stop (The Economist...).

I'm talking about the Netflix approach of wiping your account after X months of not being a paid subscriber. With Netflix this doesn't matter because their model of me is terrible at recommending me anything anyway. But with LLMs, this could be a very powerful tool for keeping people paying. (Obviously this only works if there is no free tier.)

Get the user paying a few quid a month, let it build up a history of them, then hold that hostage when they can't pay. Hell we're starting them in school anyway, so it could have _decades_ of saved knowledge about the individual. You finish school and lose that sweet subsidised cost, and you can't get no job because they aren't any and all the fish are dead and whatnot, and now it's five quid a month or it forgets you forever.

Fortunately legislation already exists to require platforms to let you export your data, but the providers will make it very difficult for you to ingest that data _back into_ the system when you re-subscribe. This also covers making it harder for users to switch between providers.

## Model quality

This has already been observed. A given model will get worse over time to nudge you towards upgrading towards the next model, or to shave cents off inference costs. To aid in this, the providers could start ommitting the exact version number. Instead of choosing between GPT 8.3 and GPT 8.4-pro and GPT 8.4-mini and GPT 8.2-turbo, you just have generic stub. "GPT", "Pro", "Mini", "Turbo". Today this seems unlikely because a new version of the model is a big marketing bump for the provider. Hey look at this new model it is better for reasons X Y and Z. But in a mature ecosystem, new versions probably don't mean much, and hiding this information from consumers will be useful. For example you could quietly downground the "Mini" from 8.4-mini to 8.3-mini because that runs more efficiently on your new compute node. Perhaps keep the major version number and use that for your marketing bump, and that's always your opportunity to increase costs.

## Selling user data

Already happening? IDK. I'm not sure if this counts as enshittification because the service itself would be unchanged, but the overall experience for the user is shitter so?

The really dark version of this is a user in a lesser developed country asks the LLM for advice on a medical condition, and the LLM sells that to the private medical providers, and then the user's insurance permium goes up. I think this is unlikely, I really hope medical data entered into an LLM gets the same legal protections as actual medical data and cannot be sold in this way.

The regulator-friendlier implementation is to train specialised models on cohorts of users and then sell access to it. So you could take all women in their 20s living in the North of England, train a model on all their chat history, and then sell that model to Palantir to help them achieve their ultimate goal of owning and inhabiting York castle[^3].

## Conclusion

Ah it's all a bit shit really isn't it.


[^1]: Disclaimer: I have not used this enough to know.
[^2]: I might eat these words. There is a small chance of a massive leap by one company, in which case all bets are off.
[^3]: IDK what Palantir does but people seem very scared of them, I took a stab in the dark.
