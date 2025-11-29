You would have already seen that changing `https://DISCOURSE_HOSTNAME/t/my-topic-name-slug/the-topic-id/` to `https://DISCOURSE_HOSTNAME/raw/5224/` meets most export needs, but what about a topic with a large number of images?

Well, that export would have `![an-image-caption|widthxheight](upload://data-base62-sha1.EXT)` wherever there is an image present, which is not the image itself.

In order to obtain all the images from `https://DISCOURSE_HOSTNAME/t/my-topic-name-slug/the-topic-id/` to `https://DISCOURSE_HOSTNAME/raw/the-topic-id/`, you need to append `.json?include_raw=1` to get `https://DISCOURSE_HOSTNAME/t/my-topic-name-slug/the-topic-id.json?include_raw=1` & **Save page as** the `<<<<<JSON filename>>>>>` placeholder in the same folder that the script is saved in.

the resulting `zip` folder will save in the same folder that the python script is saved in, and will have the following directory format

```text
images_3-random-numbers.zip
│
├── an-image-caption
│   └── width
│       └── height
│           └── w4iQtqpKsqwWONSgTXXYZS4Su8o.png
│
├── an-image-caption
│   └── width
│       └── height
│           └── pOv7GTROfxmQFHyv9KSYTe4t1vw.png
│
├── an-image-caption
│   └── width
│       └── height
│           └── yMg80bUyufaJhJ0DYlXjk5qJUR8.png
│
├── an-image-caption
│   └── width
│       └── height
│           └── AOosHsblEJnzUvcYQpjjYJ1287Q.png
│
└── (repeated for every image...)
```

where a `data-base62-sha1.EXT` is `AOosHsblEJnzUvcYQpjjYJ1287Q.png`
