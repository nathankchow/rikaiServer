# rikaiServer
Complement to rikaiClient

rikaiServer broadcasts Japanese sentence segmentation data (from [ichiran](https://github.com/tshatrov/ichiran)) of visual novel text to [rikaiClient](https://github.com/nathankchow/rikaiClient/) (iOS app). Currently, rikaiServer uses [Textractor](https://github.com/Artikash/Textractor) extended with the following [extension](https://github.com/nathankchow/Example-Extension) to harvest text from visual novels. 

rikaiServer can also export Anki cards in a CSV format to import into Anki, when prompted to from rikaiClient.

# Requirements

- ichiran-cli (compile following these [instructions](https://readevalprint.tumblr.com/post/639359547843215360/ichiranhome-2021-the-ultimate-guide))
- PostgreSQL (ichiran requirement)
- [Textractor](https://github.com/Artikash/Textractor)
- [Textractor extension](https://github.com/nathankchow/Example-Extension)
- RabbitMQ 
- [RikaiClient](https://github.com/nathankchow/rikaiClient/)

# To-Do

- Remove RabbitMQ dependency. For the time it is being used to asynchronously run ichiran-cli via multiprocesssing. Could not find a multi-threaded solution, as ichiran-cli seems to block no matter what I try.
- Find a way to hook Textractor text directly without needing the extension.
- (unlikely) Implement my very own translation/segmentation solution, or consider alternatives to ichiran.
