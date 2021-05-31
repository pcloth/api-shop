# Documentation and mock tools

::: tip 
- Api-shop provides an api interface online documentation and mock tool page based on vue and element-ui
:::

![An image](../../static/demo.png)

## Configuring document route
- In the ApiShop component instance, there is a method render_documents(request, url)
- In conjunction with it, there must be a get_api_data(request, url) method for the document to get the interface data.

``` python
# The flask example omits the conf configuration and introduces part of the code.
af = ApiShop(conf)

@app.route('/api/<regex("([\s\S]*)"):url>',methods=['GET', 'POST','PUT','DELETE','PATCH'])
def hello_world(url):
    print(url)
    if url=='documents/':
        # Configured here is the route to access the document
        return af.render_documents(request,url)
    if url=='api_data':
        # Here is the data interface required by the document.
        return af.get_api_data(request,url)
    
    return af.api_entry(request,url)
```

#### This way, you can access the online documentation via `yourhost/api/documents/` in your browser and give it to your front-end team members, which can reduce unnecessary communication.
#### The built-in online documentation also provides a simple mock tool for front-end personnel to debug the interface.


## Custom document template
::: tip
- If you are not satisfied with the document style, you can write your own document template.
:::

### Document page business process
1. After the page is loaded, please visit the api_data interface you configured to get all the interface data.
2. Render your page and configure the mock tool based on the interface packet
3. When the ApiShop is instantiated, write the actual path of the new document to the options.document project.
```python
options = {
    'document': BASE_DIR + '/static/document.html',  # Please fill in the absolute path
}
```