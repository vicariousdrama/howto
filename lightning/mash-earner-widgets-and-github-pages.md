# Mash Earning Widgets and Github Pages

## Synopsis

This guide provides some platform specific guidance for using Mash with Github
Pages and getting the site build process to work with transforms from Markdown
to the resulting HTML.

## About Mash

[Mash](https://getmash.com) is a service that allows for content providers to 
earn based on integrating assorted pay-to-access widgets into their website 
around content. Creating an account and adding widgets is pretty easy as they
offer integrations for basic Javascript to plugins for popular frameworks like
Wordpress, Wix and others.  Whether a user paying or an earner, Mash operates
as a custodial Lightning wallet that is easy to top-up with funding or spend
to withdraw sats elsewhere.

To begin earning with Mash, [sign up here](https://wallet.getmash.com/earn/sign-up)
or, [signup for a standard user wallet here](https://wallet.getmash.com/dashboard/sign-up).
You can start with a standard wallet and add details for an earner wallet later
if you'd like.  This guide assumes that you've setup the 
[earner settings](https://wallet.getmash.com/earn/settings).

## About Github Pages

[Github Pages](docs.github.com/en/pages) is a form of hosting that relies on 
static files from a repository in Github, and can optionally be created by 
processing through Jekyll and Liquid transforms to use themes and templates 
to change the look of a site with ease.

This guide assumes that you've already setup a Github account and are familiar
with publishing a site with Github Pages an actions.  For most repositories,
you can get to quick settings at 
github.com/user-or-organization-name/repository-name/settings/pages

## Integrating Mash Platform Snippet with a Site

If you are using Github pages, then after setting up an account on Mash, you
can start the process of [Connecting Your Site to Mash](https://wallet.getmash.com/earn/install).
Choose `General` when selecting a platform, determine where you want the
controller widget to appear for desktop and mobile, and you'll get presented
with your Mash Platform Snippet.  An example is depicted below that is used
on my [Nodeyez](https://nodeyez.com) website.

```html
  <script>
    window.MashSettings = {
      id: "a5c0d053-92ec-4b89-b7e4-fb089ab9b051"
    };
    var loader = function () {
      window.Mash.init();
    };
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.defer = true;
    script.onload = loader;
    script.src = "https://wallet.getmash.com/sdk/sdk.js";
    var head = document.getElementsByTagName("head")[0];
    head.appendChild(script);
  </script>
```
Follow the guidance to add YOUR snippet to your site as guided.

For a Github driven site using themes, a good place for many themes
to include this would be in the `_includes/head-custom.html` file.

## Making Use of the Widgets

From the [Mash Widget Gallery](https://wallet.getmash.com/earn/widgets),
choose the type of Widget you want to use.  You will need to select a
pay category (or define one if you haven't yet created any), and then
you'll be presented with the docs.getmash.com website which shows a
configurable example of your widget chosen.

Here's an example of the Accordion widget

![image](https://user-images.githubusercontent.com/88121568/221309909-cadb1c44-e0db-474f-9cb6-123170893e6d.png)

You should set a unique identifier value for the `key` field which will be 
used to remember if the user has previously accessed the resource. The `resource`
field should be automatically populated based on the Category ID generated 
tied to your earner account.

To get the source code for a widget, after changing any options, click on 
the Docs link within that widget group to see the same widget sample, 
including a `Show code` action button in the lower right corner

![image](https://user-images.githubusercontent.com/88121568/221310865-23f00920-15f0-474f-9129-995d314a0908.png)

Click that and you'll have your widget sample that you can copy and paste
into your markdown page. Here's a sample.  

```html
<mash-accordion key="samplekey1" resource="549a2981-ae65-41e3-b620-6b22bec143cd" button-horizontal-align="center" button-vertical-align="bottom" button-text="Read More" button-variant="solid" button-size="md" loading-indicator-size="14">
    <p>
      A purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to
      another without the burdens of going through a financial institution. Digital signatures provide part of the
      solution, but the main benefits are lost if a trusted party is still required to prevent double-spending. We
      propose a solution to the double-spending problem using a peer-to-peer network. The network timestamps
      transactions by hashing them into an ongoing chain of hash-based proof-of-work, forming a record that cannot be
      changed without redoing the proof-of-work. The longest chain not only serves as proof of the sequence of events
      witnessed, but proof that it came from the largest pool of CPU power. As long as honest nodes control the most CPU
      power on the network, they can generate the longest chain and outpace any attackers. The network itself requires
      minimal structure. Messages are broadcasted on a best effort basis, and nodes can leave and rejoin the network at
      will, accepting the longest proof-of-work chain as proof of what happened while they were gone.
    </p>
  </mash-accordion>
```

Use the custom `<mash-accordion>` tags to wrap whatever content you want to be 
behind your earner paywall.

## Tailoring to the Jekyll and Liquid Transformation Process

When you include HTML tags in markdown the build engine will allow them to persist 
through without any conversion. However, the transformation process has a few rules.

1. You should have a blank line both before and after any HTML in your markdown.
2. HTML tags should begin at the beginning of a line of text
3. Your HTML can enclose markdown.  For example, you could do this...

```markdown

## Section name

This is some text

<table>
<tr>
<td><i>column 1 is italicized</i></td><td><b>this text is bold</b></td>
</tr>
<tr>
<td colspan="2">
      
a [link text](url) inside a cell spanning two columns in a table
      
</td>
</tr>
<table>
  
```

And it would render like this 

![image](https://user-images.githubusercontent.com/88121568/221315725-1dd7f50f-5554-4d75-97be-34ff19050c2c.png)

What isn't exactly clear is that the processing engine that handles the
transforms for markdown to HTML is also analyzing the HTML tags presented
and applies various rules based on whether the tag is recognized, whether
it is a block element or inline etc.

Because the Mash Widgets are using HTML tags that aren't standard, the
conversion process may take all the content contained within, and not 
perform any transformation of nested markdown, leaving what appears to be
unformatted text as line returns.  

This can result in a poor user experience, particularly if they paid to
reveal the content.  For example, this is the output seen if no further
adjustments are taken

![image](https://user-images.githubusercontent.com/88121568/221317499-dbfb0a5e-c9a0-4b61-8917-5b9bcd655c9b.png)

But what is desired is this

![image](https://user-images.githubusercontent.com/88121568/221319173-45c26ae2-db37-4785-8bb4-42eaf67cb08e.png)



To correct for this is rather straightforward.  We add another rule to
the list above

4. Anytime a non-standard or non-widely recognized HTML tag is used to
enclose markdown, we should add the attribute `markdown="1"`, as well 
as nest its contents in another div tag denoting the same.

An updated version interspersing the `<mash-accordion>` tag into markdown
would thus be as follows:

```html
## Section name

This is some text and an HTML component will follow

<mash-accordion markdown="1" key="samplekey1" resource="549a2981-ae65-41e3-b620-6b22bec143cd" button-horizontal-align="center" button-vertical-align="bottom" button-text="Read More" button-variant="solid" button-size="md" loading-indicator-size="14">

<div markdown="1">
  
A purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to
another without the burdens of going through a financial institution. Digital signatures provide part of the
solution, but the main benefits are lost if a trusted party is still required to prevent double-spending. We
propose a solution to the double-spending problem using a peer-to-peer network. The network timestamps
transactions by hashing them into an ongoing chain of hash-based proof-of-work, forming a record that cannot be
changed without redoing the proof-of-work. The longest chain not only serves as proof of the sequence of events
witnessed, but proof that it came from the largest pool of CPU power. As long as honest nodes control the most CPU
power on the network, they can generate the longest chain and outpace any attackers. The network itself requires
minimal structure. Messages are broadcasted on a best effort basis, and nodes can leave and rejoin the network at
will, accepting the longest proof-of-work chain as proof of what happened while they were gone.

- markdown list item 1
- markdown list item 2
- markdown list item 3
  
</div>

</mash-accordion>
```

The nested `<div>` tag is a recognized HTML tag by the parser and we instruct it 
to process the markdown inside the block.  The result of that processing results 
in the transformed HTML which is the desired output we want enclosed in the custom
`<mash-accordion>` HTML tag.  

This same trick works on all the other custom HTML tags used for Mash Widgets that I've
tested thus far.




