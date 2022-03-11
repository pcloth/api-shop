(self.webpackChunkdocuments=self.webpackChunkdocuments||[]).push([[120],{1705:(n,s,t)=>{"use strict";t.r(s),t.d(s,{data:()=>a});const a={key:"v-1020f180",path:"/components/",title:"组件",lang:"zh-CN",frontmatter:{},excerpt:"",headers:[{level:2,title:"ApiShop 类组件",slug:"apishop-类组件",children:[{level:3,title:"代码中直接运行另一个api接口",slug:"代码中直接运行另一个api接口",children:[]},{level:3,title:"ApiShop conf 说明",slug:"apishop-conf-说明",children:[]},{level:3,title:"ApiShop conf methods 说明",slug:"apishop-conf-methods-说明",children:[]},{level:3,title:"ApiShop options 说明",slug:"apishop-options-说明",children:[]},{level:3,title:"ApiShop options lang_pack 说明",slug:"apishop-options-lang-pack-说明",children:[]}]},{level:2,title:"方法组件",slug:"方法组件",children:[{level:3,title:"get_api_result_json 方法（将删除）",slug:"get-api-result-json-方法-将删除",children:[]},{level:3,title:"get_api_result_response 方法（将删除）",slug:"get-api-result-response-方法-将删除",children:[]}]}],filePathRelative:"components/README.md",git:{updatedTime:1624630892e3}}},2658:(n,s,t)=>{"use strict";t.r(s),t.d(s,{default:()=>e});const a=(0,t(6252).uE)('<h1 id="组件"><a class="header-anchor" href="#组件">#</a> 组件</h1><table><thead><tr><th style="text-align:left;">模块名字</th><th style="text-align:center;">功能说明</th><th style="text-align:left;">模块介绍</th></tr></thead><tbody><tr><td style="text-align:left;">ApiShop</td><td style="text-align:center;">api初始化类</td><td style="text-align:left;">用以加载conf和options</td></tr><tr><td style="text-align:left;">api_run</td><td style="text-align:center;">ApiShop实例方法</td><td style="text-align:left;">用来在业务代码中运行别的接口(取代get_api_result_json和get_api_result_response)</td></tr><tr><td style="text-align:left;">Api</td><td style="text-align:center;">业务基础类</td><td style="text-align:left;">用来继承后写实际的业务代码</td></tr><tr><td style="text-align:left;">ApiResponseModelFields</td><td style="text-align:center;">制作包含部分model字段的response返回对象文档</td><td style="text-align:left;"></td></tr><tr><td style="text-align:left;">get_api_result_json</td><td style="text-align:center;">直接调用业务类(后面版本将删除它)</td><td style="text-align:left;">返回 json,status_code</td></tr><tr><td style="text-align:left;">get_api_result_response</td><td style="text-align:center;">直接调用业务类(后面版本将删除它)</td><td style="text-align:left;">返回response</td></tr><tr><td style="text-align:left;">data_format</td><td style="text-align:center;">内置自定义数据格式</td><td style="text-align:left;">data_format.datetime 可以将一个字符串转换成datetime格式</td></tr><tr><td style="text-align:left;">data_format.DataExpansion</td><td style="text-align:center;">自定义数据基础类</td><td style="text-align:left;">用来写自定义数据格式</td></tr></tbody></table><h2 id="apishop-类组件"><a class="header-anchor" href="#apishop-类组件">#</a> ApiShop 类组件</h2><div class="custom-container tip"><p class="custom-container-title">TIP</p><p>api-shop核心类，实例化后生成接口对象，你只需要访问实例的方法，就可以调用相应的业务代码。</p></div><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code>ap <span class="token operator">=</span> ApiShop<span class="token punctuation">(</span>conf<span class="token punctuation">,</span>options<span class="token punctuation">)</span>\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br></div></div><h3 id="代码中直接运行另一个api接口"><a class="header-anchor" href="#代码中直接运行另一个api接口">#</a> 代码中直接运行另一个api接口</h3><div class="custom-container tip"><p class="custom-container-title">TIP</p><p>从1.12.0版本开始，ApiShop核心类提供了一个api_run的方法，用来在代码中运行另外一个api代码，方便复用。 这个方法将取代原本的get_api_result_json和get_api_result_response</p></div><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code><span class="token triple-quoted-string string">&#39;&#39;&#39;\n    request   直接传入当前request，\n    url       就是你想要访问的接口url\n    method    如果不传入，就是 = request.method\n    parameter 请求参数，如果不传入，就没有参数传入到api中\n    json      默认True返回json数据，False就会返回response\n&#39;&#39;&#39;</span> \nresponse_json<span class="token punctuation">,</span>code <span class="token operator">=</span> ap<span class="token punctuation">.</span>api_run<span class="token punctuation">(</span>request<span class="token punctuation">,</span> url<span class="token punctuation">,</span> method<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">,</span> parameter<span class="token operator">=</span><span class="token punctuation">{</span><span class="token string">&#39;a&#39;</span><span class="token punctuation">:</span><span class="token number">1</span><span class="token punctuation">}</span><span class="token punctuation">,</span> json<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>\n<span class="token keyword">print</span><span class="token punctuation">(</span>response_json<span class="token punctuation">,</span>code<span class="token punctuation">)</span>\n\n<span class="token comment"># 或者直接在Api实例中使用 # Or use it directly in the Api instance</span>\n<span class="token keyword">class</span> <span class="token class-name">test_api</span><span class="token punctuation">(</span>Api<span class="token punctuation">)</span><span class="token punctuation">:</span>\n    <span class="token keyword">def</span> <span class="token function">post</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">,</span> data<span class="token punctuation">)</span><span class="token punctuation">:</span>\n        response_json<span class="token punctuation">,</span>code <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token punctuation">.</span>api_run<span class="token punctuation">(</span>request<span class="token punctuation">,</span> other_url<span class="token punctuation">,</span> method<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">,</span> parameter<span class="token operator">=</span><span class="token punctuation">{</span><span class="token string">&#39;a&#39;</span><span class="token punctuation">:</span><span class="token number">1</span><span class="token punctuation">}</span><span class="token punctuation">,</span> json<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>\n        <span class="token keyword">print</span><span class="token punctuation">(</span>response_json<span class="token punctuation">,</span>code<span class="token punctuation">)</span>\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br><span class="line-number">13</span><br><span class="line-number">14</span><br><span class="line-number">15</span><br></div></div><h3 id="apishop-conf-说明"><a class="header-anchor" href="#apishop-conf-说明">#</a> ApiShop conf 说明</h3><h4 id="apishop-conf-例子"><a class="header-anchor" href="#apishop-conf-例子">#</a> ApiShop conf 例子</h4><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code>conf <span class="token operator">=</span> <span class="token punctuation">[</span>\n    <span class="token punctuation">{</span>\n        <span class="token string">&#39;url&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;login&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;class&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;account.views.api_login&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;账户登录&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;methods&#39;</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>\n            <span class="token string">&#39;POST&#39;</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>\n                <span class="token punctuation">{</span><span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;username&#39;</span><span class="token punctuation">,</span> <span class="token string">&#39;type&#39;</span><span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">,</span> <span class="token string">&#39;required&#39;</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span> <span class="token string">&#39;min&#39;</span><span class="token punctuation">:</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token string">&#39;max&#39;</span><span class="token punctuation">:</span> <span class="token number">24</span><span class="token punctuation">,</span> <span class="token string">&#39;description&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;用户名&#39;</span><span class="token punctuation">}</span><span class="token punctuation">,</span>\n                <span class="token punctuation">{</span><span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;password&#39;</span><span class="token punctuation">,</span> <span class="token string">&#39;type&#39;</span><span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">,</span> <span class="token string">&#39;required&#39;</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span> <span class="token string">&#39;min&#39;</span><span class="token punctuation">:</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token string">&#39;max&#39;</span><span class="token punctuation">:</span> <span class="token number">24</span><span class="token punctuation">,</span> <span class="token string">&#39;description&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;密码&#39;</span><span class="token punctuation">}</span><span class="token punctuation">,</span>\n            <span class="token punctuation">]</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;GET&#39;</span><span class="token punctuation">:</span><span class="token punctuation">[</span><span class="token punctuation">]</span>\n        <span class="token punctuation">}</span>\n    <span class="token punctuation">}</span><span class="token punctuation">,</span>\n<span class="token punctuation">]</span>\n\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br><span class="line-number">13</span><br><span class="line-number">14</span><br><span class="line-number">15</span><br></div></div><h4 id="apishop-conf-详细"><a class="header-anchor" href="#apishop-conf-详细">#</a> ApiShop conf 详细</h4><table><thead><tr><th style="text-align:left;">键</th><th style="text-align:left;">值类型</th><th style="text-align:right;">说明</th></tr></thead><tbody><tr><td style="text-align:left;">url</td><td style="text-align:left;">str,list</td><td style="text-align:right;">接口的url地址，只需要填写相对地址，如果有多条url，可以配置成<code>list</code>。支持url参数：<code>/api/url/&lt;id&gt;</code></td></tr><tr><td style="text-align:left;">class</td><td style="text-align:left;">str,class</td><td style="text-align:right;">接口实际调用的业务类（继承至Api），可以是对象，也可以是引用地址</td></tr><tr><td style="text-align:left;">name</td><td style="text-align:left;">str</td><td style="text-align:right;">接口的名字</td></tr><tr><td style="text-align:left;">methods</td><td style="text-align:left;">dict</td><td style="text-align:right;">接口所能接收的methods：有GET POST DELETE PUT PATCH</td></tr></tbody></table><h3 id="apishop-conf-methods-说明"><a class="header-anchor" href="#apishop-conf-methods-说明">#</a> ApiShop conf methods 说明</h3><h4 id="apishop-conf-methods-详细"><a class="header-anchor" href="#apishop-conf-methods-详细">#</a> ApiShop conf methods 详细</h4><table><thead><tr><th style="text-align:left;">键</th><th style="text-align:left;">值类型</th><th style="text-align:right;">说明</th></tr></thead><tbody><tr><td style="text-align:left;">name</td><td style="text-align:left;">str</td><td style="text-align:right;">参数名，接收后在data.name</td></tr><tr><td style="text-align:left;">type</td><td style="text-align:left;">class</td><td style="text-align:right;">str,int,float,bool,list,dict,tuple等等，也支持data_format.datetime时间格式，你也可以自定义一个类型转换器</td></tr><tr><td style="text-align:left;">required</td><td style="text-align:left;">bool</td><td style="text-align:right;">是否是必要值</td></tr><tr><td style="text-align:left;">default</td><td style="text-align:left;">str,function</td><td style="text-align:right;">当没有接收到时的默认值，注意，它也会被type所指定的类型转换器转换。当它是一个function时，如果没有收到请求参数，将会自动运行这个方法获取值，同时将不再进行类型转换。</td></tr><tr><td style="text-align:left;">min</td><td style="text-align:left;">int,str</td><td style="text-align:right;">最小值/最小长度，为字符串时，会被type指定的类型转换器转换。</td></tr><tr><td style="text-align:left;">max</td><td style="text-align:left;">int,str</td><td style="text-align:right;">最大值/最大长度，为字符串时，会被type指定的类型转换器转换。</td></tr><tr><td style="text-align:left;">description</td><td style="text-align:left;">str</td><td style="text-align:right;">功能描述，给前端人员看文档的内容</td></tr><tr><td style="text-align:left;">options</td><td style="text-align:left;">list</td><td style="text-align:right;">参数必须在这个列表中的值，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request</td></tr></tbody></table><h3 id="apishop-options-说明"><a class="header-anchor" href="#apishop-options-说明">#</a> ApiShop options 说明</h3><h4 id="apishop-options-例子"><a class="header-anchor" href="#apishop-options-例子">#</a> ApiShop options 例子</h4><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code>options <span class="token operator">=</span> <span class="token punctuation">{</span>\n                <span class="token string">&#39;base_url&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;/api/&#39;</span><span class="token punctuation">,</span>\n                <span class="token string">&#39;bad_request&#39;</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span>\n                <span class="token string">&#39;document&#39;</span><span class="token punctuation">:</span> BASE_DIR <span class="token operator">+</span> <span class="token string">&#39;/api_shop/static/document.html&#39;</span><span class="token punctuation">,</span> \n                <span class="token string">&#39;lang&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;en&#39;</span><span class="token punctuation">,</span>\n                <span class="token string">&#39;lang_pack&#39;</span><span class="token punctuation">:</span><span class="token punctuation">{</span><span class="token punctuation">}</span>\n            <span class="token punctuation">}</span>\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br></div></div><h4 id="apishop-options-详细"><a class="header-anchor" href="#apishop-options-详细">#</a> ApiShop options 详细</h4><table><thead><tr><th style="text-align:left;">键</th><th style="text-align:left;">值类型</th><th style="text-align:left;">默认值</th><th style="text-align:right;">说明</th></tr></thead><tbody><tr><td style="text-align:left;">base_url</td><td style="text-align:left;">str</td><td style="text-align:left;">/api/</td><td style="text-align:right;">接口url前缀</td></tr><tr><td style="text-align:left;">bad_request</td><td style="text-align:left;">bool</td><td style="text-align:left;">True</td><td style="text-align:right;">如果请求不合法，是否以坏请求方式返回；否则就是全部是200返回</td></tr><tr><td style="text-align:left;">bad_request_error_status</td><td style="text-align:left;">str,int,bool</td><td style="text-align:left;">&#39;error&#39;</td><td style="text-align:right;">如果bad_request参数设置为False，那么这个参数就会启用，会在坏请求里附带一个status=&#39;error&#39;的信息，你可以自定义这个信息。</td></tr><tr><td style="text-align:left;">document</td><td style="text-align:left;">str(path)</td><td style="text-align:left;">略</td><td style="text-align:right;">文档页面的html模板所在的路径，默认会有一个简易模板</td></tr><tr><td style="text-align:left;">lang</td><td style="text-align:left;">str</td><td style="text-align:left;">en</td><td style="text-align:right;">多国语言支持，目前内置en, zh</td></tr><tr><td style="text-align:left;">lang_pack</td><td style="text-align:left;">dict</td><td style="text-align:left;">无</td><td style="text-align:right;">扩展语言包，如果你想让api-shop支持更多语言</td></tr><tr><td style="text-align:left;">name_classification</td><td style="text-align:left;">list</td><td style="text-align:left;">无</td><td style="text-align:right;">用于默认的文档模板对接口名称进行过滤，便于查找</td></tr><tr><td style="text-align:left;">url_classification</td><td style="text-align:left;">list</td><td style="text-align:left;">无</td><td style="text-align:right;">用于默认的文档模板对接口url进行过滤，便于查找。例子：&#39;url_classification&#39;:[&#39;weixin&#39;,&#39;login&#39;]</td></tr><tr><td style="text-align:left;">auto_create_folder</td><td style="text-align:left;">bool</td><td style="text-align:left;">False</td><td style="text-align:right;">自动创建文件夹，debug参数也必须为True才可以生效。</td></tr><tr><td style="text-align:left;">auto_create_file</td><td style="text-align:left;">bool</td><td style="text-align:left;">False</td><td style="text-align:right;">自动创建文件，debug参数也必须为True才可以生效。</td></tr><tr><td style="text-align:left;">auto_create_class</td><td style="text-align:left;">bool</td><td style="text-align:left;">False</td><td style="text-align:right;">自动创建类，debug参数也必须为True才可以生效。</td></tr><tr><td style="text-align:left;">auto_create_method</td><td style="text-align:left;">bool</td><td style="text-align:left;">False</td><td style="text-align:right;">自动创建方法，debug参数也必须为True才可以生效。</td></tr><tr><td style="text-align:left;">framework</td><td style="text-align:left;">str</td><td style="text-align:left;">无</td><td style="text-align:right;">手动指定框架，目前支持django、flask、bottle，如果不指定，将按顺序识别框架，如果同时安装了多个框架，请手动指定。</td></tr><tr><td style="text-align:left;">debug</td><td style="text-align:left;">bool</td><td style="text-align:left;">True</td><td style="text-align:right;">加载api业务代码的时候，遇到错误抛出。</td></tr></tbody></table><h3 id="apishop-options-lang-pack-说明"><a class="header-anchor" href="#apishop-options-lang-pack-说明">#</a> ApiShop options lang_pack 说明</h3><h4 id="apishop-options-lang-pack-例子"><a class="header-anchor" href="#apishop-options-lang-pack-例子">#</a> ApiShop options lang_pack 例子</h4><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code><span class="token string">&#39;lang_pack&#39;</span><span class="token punctuation">:</span><span class="token punctuation">{</span>\n    <span class="token string">&#39;zh&#39;</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>\n            <span class="token string">&#39;no attributes found&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;没有找到属性：&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;not found in conf&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;在conf参数中没找到方法: &#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;no such interface&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;没有这个接口&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;is required&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;是必要的&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;parameter&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;参数&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;can not be empty&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;不能为空&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;must be type&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;必须是类型&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;minimum length&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;最小长度&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;minimum value&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;最小值&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;maximum length&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;最大长度&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;maximum value&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;最大值&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;The wrong configuration, methons must be loaded inside the list container.&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;错误的配置，methons必须装的list容器内。&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;no such interface method&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;这个接口没有这个method&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;Framework version is not compatible.&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;api-shop不支持当前框架版本。&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;Not support&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;不支持&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;supported framework as follows:&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;支持的框架如下：&#39;</span><span class="token punctuation">,</span>\n            <span class="token string">&#39;Did not find the framework&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;没找指定的框架，请安装&#39;</span><span class="token punctuation">,</span>\n        <span class="token punctuation">}</span>\n<span class="token punctuation">}</span>\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br><span class="line-number">13</span><br><span class="line-number">14</span><br><span class="line-number">15</span><br><span class="line-number">16</span><br><span class="line-number">17</span><br><span class="line-number">18</span><br><span class="line-number">19</span><br><span class="line-number">20</span><br><span class="line-number">21</span><br></div></div><h2 id="方法组件"><a class="header-anchor" href="#方法组件">#</a> 方法组件</h2><h3 id="get-api-result-json-方法-将删除"><a class="header-anchor" href="#get-api-result-json-方法-将删除">#</a> get_api_result_json 方法（将删除）</h3><div class="custom-container tip"><p class="custom-container-title">TIP</p><ul><li>直接调用业务代码类，获取返回数据和状态码</li><li>请注意：由于绕开了参数监测，所有参数都必须填写在data中，没有的用None填写</li></ul></div><h4 id="flask-例子"><a class="header-anchor" href="#flask-例子">#</a> flask 例子</h4><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code><span class="token keyword">from</span> api_shop <span class="token keyword">import</span> get_api_result_json\n\n<span class="token keyword">from</span> views <span class="token keyword">import</span> api_login <span class="token comment"># 继承了Api类的业务代码</span>\n\n<span class="token decorator annotation punctuation">@simple_page<span class="token punctuation">.</span>route</span><span class="token punctuation">(</span><span class="token string">&#39;/test&#39;</span><span class="token punctuation">)</span>\n<span class="token keyword">def</span> <span class="token function">hello_world</span><span class="token punctuation">(</span>url<span class="token punctuation">)</span><span class="token punctuation">:</span>\n    \n    data <span class="token operator">=</span> get_api_result_json<span class="token punctuation">(</span>\n        api_login<span class="token punctuation">,</span> <span class="token string">&#39;POST&#39;</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;testuser&#39;</span><span class="token punctuation">,</span><span class="token string">&#39;password&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;12345&#39;</span><span class="token punctuation">}</span>\n        <span class="token punctuation">)</span>\n    <span class="token keyword">print</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span> <span class="token comment"># 这样在程序内部也能快速的调用业务代码。</span>\n\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br></div></div><div class="custom-container tip"><p class="custom-container-title">get_api_result_json 参数说明</p><ul><li>get_api_result_json(api_class, method, data=None, request=None, not200=True)</li><li>直接调用api代码，并拿到返回json <ul><li>api_class 是业务api类的对象（不是实例）</li><li>method 是请求方法,str格式</li><li>data 是附加数据，dict格式</li><li>request=None 是当前request,如果method和request.method不相同，请自己封装一个适合业务代码用的request，如果业务代码不用reqeust，请不要传入。</li><li>not200=True 是允许status_code不等于200的结果，为False的时候，遇到200以外程序中断并抛错</li></ul></li><li>return json,status_code</li></ul></div><h3 id="get-api-result-response-方法-将删除"><a class="header-anchor" href="#get-api-result-response-方法-将删除">#</a> get_api_result_response 方法（将删除）</h3><div class="custom-container tip"><p class="custom-container-title">TIP</p><ul><li>直接调用业务代码类，获取返回响应包response</li><li>请注意：由于绕开了参数监测，所有参数都必须填写在data中，没有的用None填写</li></ul></div><h4 id="flask-例子-1"><a class="header-anchor" href="#flask-例子-1">#</a> flask 例子</h4><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code><span class="token keyword">from</span> api_shop <span class="token keyword">import</span> get_api_result_response\n\n<span class="token keyword">from</span> views <span class="token keyword">import</span> api_login <span class="token comment"># 继承了Api类的业务代码</span>\n\n<span class="token decorator annotation punctuation">@simple_page<span class="token punctuation">.</span>route</span><span class="token punctuation">(</span><span class="token string">&#39;/test&#39;</span><span class="token punctuation">)</span>\n<span class="token keyword">def</span> <span class="token function">hello_world</span><span class="token punctuation">(</span>url<span class="token punctuation">)</span><span class="token punctuation">:</span>\n    \n    response <span class="token operator">=</span> get_api_result_response<span class="token punctuation">(</span>\n        api_login<span class="token punctuation">,</span> <span class="token string">&#39;POST&#39;</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;testuser&#39;</span><span class="token punctuation">,</span><span class="token string">&#39;password&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;12345&#39;</span><span class="token punctuation">}</span>\n        <span class="token punctuation">)</span>\n    <span class="token keyword">print</span><span class="token punctuation">(</span>response<span class="token punctuation">)</span> <span class="token comment"># 这样在程序内部也能快速的调用业务代码。</span>\n\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br></div></div><div class="custom-container tip"><p class="custom-container-title">TIP</p><p>和get_api_result_json方法是一样的，不过get_api_result_response的返回值是一个response</p></div>',35),e={render:function(n,s){return a}}}}]);