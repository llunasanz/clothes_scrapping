# Data engineer test

## The task

Imagine we are a company that wants to provide their customers with the piece of clothing that fits the best their
style.
Every day, we add new suppliers, so we can provide more variety for our customer.
Next we want to add [scalpers](https://en.gb.scalperscompany.com/) to our catalog, for that we need to get all their
products data, so we can run it through our recommendation system and offer it to our customers.

Our pipelines for web scrapping will be run as an on-demand batch job in a serverless deployment, so we need to have a
way to automatically install the dependencies in the deployment and have a clear structure to be able to have an entry
point for the docker image.

Your task is to modify [scrap.py](scrapper%2Fscrap.py) to be able to scrap a list of products from this
webpage https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060.
Which is the "skirts" from the woman clothing collection from [scalpers](https://en.gb.scalperscompany.com/).

![untitled.png](assets/untitled.png)

In case the link is broken, we are looking to see your abilities to write code to extract data from the web. So any
collection of products from that shop will also do.

The output should be a json with the list of all the skirts. You can look at `schema/product.py` to have an idea of the
output format.
The format is quite minimal, so you are welcome to improve it in the way you think it would make sense based on the data
available in the webpage for each product.

Using [this product](https://en.gb.scalperscompany.com/products/bbcstudio24-50505-strapless-linen-dress-ss24-red) as
input, an example of how the output looks like for our schema is the next:

```json
{
  "roduct_url": "https://en.gb.scalperscompany.com/products/bbcstudio24-50505-strapless-linen-dress-ss24-red",
  "product_name": "LINEN MIDI DRESS WITH DRAPED CHEST",
  "sku": "8445279814248",
  "metadata": [
    "Made of 100% cotton",
    "Regular fit",
    "Square neckline",
    "Zip fastening",
    "Thin straps with ruffle detail"
  ],
  "images": [
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBC-50505-RED-2_8392707e-c459-4eb2-b8d5-20dd3bba8b2c.jpg?v=1715950630",
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBC-50505-RED-2_8392707e-c459-4eb2-b8d5-20dd3bba8b2c_800x.jpg?v=1715950630",
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBC-50505-RED-1_12cca2fa-3e2c-4e18-b145-927e0cae6c1b.jpg?v=1715950630",
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBC-50505-RED-1_12cca2fa-3e2c-4e18-b145-927e0cae6c1b_800x.jpg?v=1715950630",
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBC-50505-RED-3_70b33f83-8a5d-4604-8cfe-d342011d122e.jpg?v=1715950630",
    "https://en.gb.scalperscompany.com/cdn/shop/files/BBC-50505-RED-3_70b33f83-8a5d-4604-8cfe-d342011d122e_800x.jpg?v=1715950630"
  ],
  "price": "£104",
  "sizes": [
    "XS",
    "S",
    "M",
    "L",
    "XS",
    "S",
    "M",
    "L"
  ],
  "cloth_type": "dress"
}
```

Yet again if you think the schema can be improved, feel free to do so.

You can see a minimal code example with beautifulSoup4 in `scrapper/scrap.py` that can successfully scrap
the `product_name` for the product above.

You don't need to use BS4 if you don't feel comfortable with it, we just show an example that it can be done with it.
Make this repository yours and use the tools that will make you succeed in the task!

If you have enough time it would be nice to see the type of clothing as a parameters for the script so for example you
could run `python -m scrap --type skirts` or `python -m scrap --type shirts` and returns all the clothes for skirts or
shirts, respectively.

## How to proceed?

To install the dependencies use whatever you feel like, we use [poetry](https://python-poetry.org/) for dependency
management, but you can also use the provided requirements file.
We give you a set of tools that we use to start the work, but you don't need to use the same libraries as us, if you
feel
more comfortable using another dependencies feel free to continue the work with them!

Feel free to use any tool you want, that includes any IDE, Copilot, chatGPT, etc. It's not required, and it's not
necessary if you don't want to.

You should not spend more than 2-3h working on this project as that should be enough to show how you structure your
work.

All the code should be in english, including comments.

### Once you finish the project

Zip the folder content including the .git folder, so we can see the commit history.
DON'T include `.venv`,`__pychache__`,`.idea`,etc. folders as they clutter the directory. Basically anything that would be included in a `.gitignore` file.

Be sure that you added instructions of how to run your code and the code is functional.

After you send the code back to us, we will have a session with you to review the work, so you get a chance to explain
your process and add whatever you think is relevant.
We will share our feedback about the code and talk about what we liked, what we didn't like, etc.

## What are we looking for?

Don't worry if you don't get to finish the task in the timeframe we want to see how you approach the problem.

* We want to see a clear commit history that reflects the process of your work.
* Clean code. It doesn't mean every method and class needs comments. If the code is self-explanatory that's enough.
* Following common development standards so a well-structured code and architecture is welcomed.