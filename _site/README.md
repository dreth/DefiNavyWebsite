# DeFi⚓Navy website

Hi and welcome to the DeFi Navy website repo. Here we have the code and content for the entire site. 

To visualize the site locally and be able to make changes to it you need to have the following packages installed on your computer:

- [Ruby](https://www.ruby-lang.org/en/downloads/)
- [Jekyll](https://jekyllrb.com/docs/installation/) (it's a ruby gem, so `gem install jekyll` is enough)

After this, clone the repo on your pc:

```bash
git clone https://github.com/DefiNavy/website
```

Then open the console where you cloned the repo after cloning and install all the packages using `bundle install`

```bash
bundle install
```

Then run the local server to be able to make changes to the pages as you edit:

```bash
bundle exec jekyll serve
```

Make your changes!

As long as `bundle exec jekyll serve` is running, you can locally see changes to the page on `http://127.0.0.1:4000/` (or whatever local address you have configured) and the changes will be reflected on the `_site` folder, which is where all the changes made to pages are compiled to html files.

