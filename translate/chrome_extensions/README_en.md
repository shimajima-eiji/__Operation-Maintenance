# URL
-[Demo Page (Github Pages)] (https://shimajima-eiji.github.io/__Operation-Maintenance/translate/chrome_extensions)
-[GAS repository] (https://github.com/shimajima-eiji/--GAS_v5_Translate)

# Leave the translated records and history
Save history by curl to GAS with UI like PC version translation function

- Translation UI is index.html
- The function to leave a history is GAS
- Translation processing is also GAS

# Pre-setting
Clone the file and put the GAS script ID in `SCRIPT_ID =''` in `translate.js`. <br />
Once you put it in, you can run it as it is.

For details, please see the relevant repository, but GAS after forking also needs to be set.

# How to use
As per the demo page. <br />
The operation of the demo page can also be executed with chrome extensions (ver3).

## manifest.json
If you want to use version 2 for some reason,

```
  "manifest_version": 3,
  "action": {
```

of

```
  "manifest_version": 2,
  "browser_action": {
```

Please change to.
At the time of writing, I changed from version 2 to version 3, so I think it will probably work.

## index.html
Currently, only English-Japanese and Japanese-English translations are supported. <br />
I can translate other languages ​​as a specification, but I don't do it as a control (because there is no demand for me).

We translate line by line, but we also support translation of long sentences to some extent. <br />
However, the accuracy is not high because I don't care about the connection between the preceding and following sentences.

# caution
As mentioned in detail later, the Language API has a limited number of times. <br />
The one published on the demo page is the real one published for the demo, so when the Language API is called, the bang bang counter is turned. <br />
"When and what data is sent from where" is logged so that it is okay to shake off the counter. (This is the true value of this app)

You can use it in the demo state if you use it within the range of common sense, but if you want to translate a large amount of data, please use Google or DeepL obediently. <br />
Or, if you create your own environment, you can avoid the limit of the number of times.

# How to register as a # Chrome extension
This app is for personal use (if it is used by an unspecified number of people as it is, there is a high possibility that it will not be usable due to the limit on the number of Language APIs), so I have not applied for it in the app store. <br />
Since registration costs are required in the first place, it is not particularly necessary unless it is for affiliate purposes, and if the number of users increases even for affiliate purposes, it will not be possible to use it due to the above restrictions. <br />
You can also use the trick of creating multiple accounts, changing the endpoints individually, and registering some, but what about that? I don't feel like that.

** I am not responsible for any problems caused by using this script, or reprinting or making a profit as described above. ** **

# About Money Tize
I think that some people think that it is a function that should be provided and published for a fee, but I was also thinking of publishing it for a fee. <br />
However, there is also a reason why it is open to the public for free. <br />
We made this available for free because we want the translation data used here to be natural data for use as teaching material data for AI development. <br />
"You can use it for free, but please give me the data." (However, since there is a limit on the number of times, I would like to ask within the range of common sense)

This section is just about monetization, so I will mention it, but if you want to use it for free but do not want to give data, the source code is open to the public, so please build your own environment and use it.
