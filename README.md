# Clothes scrapping

Web scrapping use case from a data engineer test. The original data tests is in the zip file "original_test.zip".

# Index

1. Test README file
2. Directory tree
3. Function dictionaries


# 1. Test README file
 

## The task

We are dedicated to offering our customers clothing that perfectly matches their unique style.
Also, we continuously add new suppliers every day to ensure a greater variety for our customers.
It is planned to include [Scalpers](https://en.gb.scalperscompany.com/) to our catalog. To do this, we need to gather all their product data. This will allow us to run it through our recommendation system and offer their products to our customers.

Our web scraping pipelines will run as on-demand batch jobs in a serverless deployment. Therefore, we need an automated process to install dependencies during deployment and maintain a clear structure to establish an entry point for the Docker image.

Your task is to modify [scrap.py](scrapper%2Fscrap.py) to be able to scrap a list of products from this
webpage https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060.
Which is the "skirts" from the woman clothing collection from [scalpers](https://en.gb.scalperscompany.com/).

![untitled.png](assets/untitled.png)

If the link is broken, we want to evaluate your ability to write code for extracting data from the web. Any collection of products from that shop will be acceptable.

The output should be a JSON containing a list of all the skirts. You can refer to schema/product.py for the output format. The format is minimal, so feel free to enhance it based on the available data for each product on the webpage.

Using [this product](https://en.gb.scalperscompany.com/products/bbcstudio24-50505-strapless-linen-dress-ss24-red) as
input, an example of how the output looks like for our schema is the next:

```json
{
  "product_url": "https://en.gb.scalperscompany.com/products/40459-bach-dress-aw2324-black",
  "product_name": "MIDI DRESS WITH LUREX PAISLEY",
  "sku": "8445279630145",
  "metadata": [
    "Made of flowing fabric with metallic yarn detailing",
    "Regular fit",
    "V-neck",
    "Long sleeves with elastic cuffs",
    "Ruffle detail"
  ],
  "images": [
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-1_2ff64361-5f85-43c6-b790-4998f8aa4ab9.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-2_600f1302-48ad-4a3f-b7b1-6e17a99bfdf8.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-3_59d6b46e-2df9-49fa-8940-0b88778fc94b.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-4_45a36c3f-e4ed-4170-80d4-133d331f8ae7.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-5_d9444e24-4c4c-4a38-bfce-e28f0160a2fa.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-6_50e501b8-4a1d-445b-8a86-0025132e88e0.jpg?v=1715949942",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-S-1_e5b4df3b-b33e-4e7c-9538-08d09a25c10f.jpg?v=1715949942",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-S-2_41616034-59bc-4e6b-8a4b-0d4fd517d66d.jpg?v=1715949944",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-1_2ff64361-5f85-43c6-b790-4998f8aa4ab9_250x.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-1_2ff64361-5f85-43c6-b790-4998f8aa4ab9_800x.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-2_600f1302-48ad-4a3f-b7b1-6e17a99bfdf8_800x.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-3_59d6b46e-2df9-49fa-8940-0b88778fc94b_800x.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-4_45a36c3f-e4ed-4170-80d4-133d331f8ae7_800x.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-5_d9444e24-4c4c-4a38-bfce-e28f0160a2fa_800x.jpg?v=1715949943",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-P-6_50e501b8-4a1d-445b-8a86-0025132e88e0_800x.jpg?v=1715949942",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-S-1_e5b4df3b-b33e-4e7c-9538-08d09a25c10f_800x.jpg?v=1715949942",
    "https://en.gb.scalperscompany.com/cdn/shop/files/40459-BLACK-S-2_41616034-59bc-4e6b-8a4b-0d4fd517d66d_800x.jpg?v=1715949944"
  ],
  "currency": "GBP (£)",
  "date_time_of_conversion": "2024-07-07 12:35:31",
  "price_in_EUR": 94.2,
  "price_in_GBP": 79.9,
  "price_in_USD": 102.24,
  "sizes": [
    "XS",
    "S",
    "M",
    "L"
  ],
  "colours": [
    "BLACK"
  ]
}
```

Once again, if you think the schema can be improved, feel free to make enhancements as you see fit.

You can find a minimal code example using BeautifulSoup4 in scrapper/scrap.py, which successfully scrapes the product_name for the product mentioned above.

You don’t need to use BeautifulSoup if you’re not comfortable with it. We've provided an example, but feel free to use any tools that will help you succeed in the task. Make this repository your own!

If you have enough time, it would be great to add clothing type as a parameter for the script. For example, you could run python -m scrap --type skirts or python -m scrap --type shirts, and it would return all the items for skirts or shirts, respectively.

## How to proceed?

To install dependencies, feel free to use any method you prefer. We use [Poetry](https://python-poetry.org/ for dependency management, but you can also use the provided requirements file. We've provided a set of tools to start with, but you don't need to use the same libraries. If you're more comfortable with different dependencies, feel free to continue the work with them!

Feel free to use any tools you prefer, including any IDE, Copilot, or ChatGPT. It's not required, so use them only if you want to.

You should aim to spend no more than 2-3 hours on this project, as that should be sufficient to demonstrate how you structure your work.

All code, including comments, should be in English.

### Once you finish the project

Please zip the folder contents, including the .git folder so we can review the commit history. Exclude folders like .venv, __pycache__, .idea, and anything typically included in a .gitignore file to keep the directory clean.

Make sure to include instructions on how to run your code, and ensure that the code is functional.

After you submit the code, we’ll have a session to review your work. This will give you the opportunity to explain your process and share any relevant insights. We’ll provide feedback on what we liked and what could be improved.

## What are we looking for?

Don’t worry if you don’t finish the task within the timeframe. We want to see how you approach the problem.

* We want to see a clear commit history that reflects your work process.
* Clean code is essential. Not every method and class needs comments; if the code is self-explanatory, that’s sufficient.
* Following common development standards is important, so well-structured code and architecture are welcomed.


# 2. Directory tree

```
.
├── Dockerfile
├── Makefile
├── README.md
├── app
│   ├── __init__.py
│   └── modules
│       ├── __init__.py
│       ├── get_all_products_from_collection.py
│       └── get_all_products_from_shop.py
├── assets
│   └── untitled.png
├── infra
│   └── get_last_price.sh
├── original_test.zip
├── pyproject.toml
├── requirements.txt
├── schema
│   └── product.py
├── src
│   ├── __init__.py
│   ├── links_getter
│   │   ├── __init__.py
│   │   ├── get_all_collection_links.py
│   │   ├── get_all_products_links.py
│   │   └── get_product_links_from_page.py
│   ├── scrapper
│   │   ├── __init__.py
│   │   └── scrap.py
│   └── test
│       └── get_link_first_product.py
└── tests
    ├── assets
    │   └── example_skirt_000.html
    ├── test__app__modules__get_all_products_from_collection.py
    ├── test__infra__get_last_price.sh
    ├── test__src__links_getter__get_all_collection_links.py
    ├── test__src__links_getter__get_all_products_links.py
    ├── test__src__links_getter__get_product_links_from_page.py
    ├── test__src__scrapper__scrap.py
    └── test__unit__get_link_first_product.py

```


# 3. Function dictionaries

## src

### links\_getter

#### get\_product\_links\_from\_page.py
This function return an array of URL products retrieving only the links with status 200. The input is an URL from a collection page.

#### get\_all\_products\_links.py
Similar to the previous function but retieving all products URLs at shop homepage.

#### get\_all\_collection\_links.py
It is almost the same function as the previous one. In this case, it returns an array of collection URLs.

### scrap

#### scrapper.py
The function that get all the product information by scrapping the product page URL. The product data is stored in a dictionary.

Here is an example of its output:
```
{
  "product_url": "https://en.gb.scalperscompany.com/products/bbcstudioii24-50909-ruffle-print-dress-ss24-fucsia",
  "product_name": "LONG CUT-OUT DRESS",
  "sku": "8445279342154",
  "metadata": [
    "Made of flowing fabric",
    "Slim fit",
    "Zip fastening",
    "V-neck",
    "Ruffled sleeves"
  ],
  "images": [
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBCII-50909-FUCSIA-1.jpg?v=1719312959",
    "https://en.gb.scalperscompany.com/cdn/shop/files/50909-FUCSIA-S-1_5d457a51-23be-4483-9c63-242171b20c30.jpg?v=1719312959",
    "https://en.gb.scalperscompany.com/cdn/shop/files/50909-FUCSIA-S-2_69903cad-7de3-4e3e-987d-3b05ddec904e.jpg?v=1719312959",
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBCII-50909-FUCSIA-1_250x.jpg?v=1719312959",
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBCII-50909-FUCSIA-1_800x.jpg?v=1719312959",
    "https://en.gb.scalperscompany.com/cdn/shop/files/50909-FUCSIA-S-1_5d457a51-23be-4483-9c63-242171b20c30_250x.jpg?v=1719312959",
    "https://en.gb.scalperscompany.com/cdn/shop/files/50909-FUCSIA-S-1_5d457a51-23be-4483-9c63-242171b20c30_800x.jpg?v=1719312959",
    "https://en.gb.scalperscompany.com/cdn/shop/files/50909-FUCSIA-S-2_69903cad-7de3-4e3e-987d-3b05ddec904e_800x.jpg?v=1719312959"
  ],
  "price": "£124",
  "sizes": [
    "XS",
    "S",
    "M",
    "L"
  ],
  "colours": [
    "FUCSIA"
  ]
}
```

## infra
### get\_last\_price.sh
Bash script to get the most recent price from stock or currency exchange via Google Finance webpage.

## app
#### get\_all\_products\_from\_collection.py
This script runs recursively `scrapper.py` to get an array of product data from all collection items.

#### get\_all\_products\_from\_shop.py
It do the same as `get\_all\_products\_from\_collection.py` but iterating on all unique collection URLs.
Supported shops:
- https://en.gb.scalperscompany.com
- https://en.ww.scalperscompany.com
