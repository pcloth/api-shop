(self.webpackChunkdocuments=self.webpackChunkdocuments||[]).push([[300],{9574:(n,s,a)=>{"use strict";a.r(s),a.d(s,{data:()=>t});const t={key:"v-08e0d16d",path:"/components/data_format.html",title:"数据类型扩展",lang:"zh-CN",frontmatter:{title:"数据类型扩展"},excerpt:"",headers:[{level:2,title:"data_format 扩展",slug:"data-format-扩展",children:[{level:3,title:"data_format.datetime",slug:"data-format-datetime",children:[]},{level:3,title:"data_format.regex 正则格式校验",slug:"data-format-regex-正则格式校验",children:[]},{level:3,title:"内置更多的快速正则校验",slug:"内置更多的快速正则校验",children:[]},{level:3,title:"data_format.DataExpansion 自定义数据类型",slug:"data-format-dataexpansion-自定义数据类型",children:[]}]}],filePathRelative:"components/data_format.md",git:{updatedTime:1624630892e3}}},9976:(n,s,a)=>{"use strict";a.r(s),a.d(s,{default:()=>p});const t=(0,a(6252).uE)('<h2 id="data-format-扩展"><a class="header-anchor" href="#data-format-扩展">#</a> data_format 扩展</h2><div class="custom-container tip"><p class="custom-container-title">数据格式扩展</p><ul><li>data_format.datetime 可以用来填写在conf.methods参数列表中的type，将request参数中的字符串<code>&quot;2019-01-01 08:30:00&quot;</code>转换成datetime格式</li><li>data_format.DataExpansion 自定义扩展基础类</li></ul></div><h3 id="data-format-datetime"><a class="header-anchor" href="#data-format-datetime">#</a> data_format.datetime</h3><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code><span class="token keyword">from</span> api_shop <span class="token keyword">import</span> data_format\nconf <span class="token operator">=</span> <span class="token punctuation">[</span>\n    <span class="token punctuation">{</span>\n        <span class="token string">&#39;url&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;test&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;class&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;account.views.api_test&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;测试方法&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;methods&#39;</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>\n            <span class="token string">&#39;POST&#39;</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>\n                <span class="token punctuation">{</span><span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;time&#39;</span><span class="token punctuation">,</span> <span class="token string">&#39;type&#39;</span><span class="token punctuation">:</span> data_format<span class="token punctuation">.</span>datetime<span class="token punctuation">,</span> <span class="token string">&#39;required&#39;</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span> <span class="token string">&#39;min&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;2018-01-01&#39;</span><span class="token punctuation">,</span> <span class="token string">&#39;max&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;2019-12-31&#39;</span><span class="token punctuation">,</span> <span class="token string">&#39;description&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;时间&#39;</span><span class="token punctuation">}</span>\n            <span class="token punctuation">]</span><span class="token punctuation">,</span>\n        <span class="token punctuation">}</span>\n    <span class="token punctuation">}</span><span class="token punctuation">,</span>\n<span class="token punctuation">]</span>\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br><span class="line-number">13</span><br></div></div><h4 id="提交请求的时候-会把传入的time参数转换成datetime格式-并检查是否大于等于2018年1月1日-小于等于2019年12月31日。"><a class="header-anchor" href="#提交请求的时候-会把传入的time参数转换成datetime格式-并检查是否大于等于2018年1月1日-小于等于2019年12月31日。">#</a> 提交请求的时候，会把传入的time参数转换成datetime格式，并检查是否大于等于2018年1月1日，小于等于2019年12月31日。</h4><h3 id="data-format-regex-正则格式校验"><a class="header-anchor" href="#data-format-regex-正则格式校验">#</a> data_format.regex 正则格式校验</h3><p>将对上传的字符串进行正则校验。 调用方法：</p><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code><span class="token keyword">from</span> src<span class="token punctuation">.</span>api_shop <span class="token keyword">import</span> data_format\n\nconf <span class="token operator">=</span> <span class="token punctuation">[</span>\n    <span class="token punctuation">{</span>\n        <span class="token string">&#39;url&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;test&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;class&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;business_code.views.api_test&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;测试接口&#39;</span><span class="token punctuation">,</span>\n        <span class="token string">&#39;methods&#39;</span><span class="token punctuation">:</span> <span class="token punctuation">{</span>\n            <span class="token string">&#39;POST&#39;</span><span class="token punctuation">:</span> <span class="token punctuation">[</span>\n                <span class="token punctuation">{</span><span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;email&#39;</span><span class="token punctuation">,</span> \n                    <span class="token string">&#39;type&#39;</span><span class="token punctuation">:</span> data_format<span class="token punctuation">.</span>regex<span class="token punctuation">(</span>\n                        <span class="token string">r&#39;^[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+){0,4}$&#39;</span><span class="token punctuation">,</span>name<span class="token operator">=</span><span class="token string">&#39;邮箱&#39;</span><span class="token punctuation">)</span><span class="token punctuation">,</span> \n                    <span class="token string">&#39;required&#39;</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span> \n                    <span class="token string">&#39;min&#39;</span><span class="token punctuation">:</span> <span class="token number">6</span><span class="token punctuation">,</span> \n                    <span class="token string">&#39;max&#39;</span><span class="token punctuation">:</span> <span class="token number">24</span><span class="token punctuation">,</span> \n                    <span class="token string">&#39;description&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;邮箱&#39;</span>\n                <span class="token punctuation">}</span><span class="token punctuation">,</span>\n                <span class="token punctuation">{</span><span class="token string">&#39;name&#39;</span><span class="token punctuation">:</span><span class="token string">&#39;idcard&#39;</span><span class="token punctuation">,</span> <span class="token string">&#39;type&#39;</span><span class="token punctuation">:</span> data_format<span class="token punctuation">.</span>idcard<span class="token punctuation">,</span> <span class="token string">&#39;required&#39;</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span> <span class="token string">&#39;description&#39;</span><span class="token punctuation">:</span> <span class="token string">&#39;身份证&#39;</span><span class="token punctuation">}</span><span class="token punctuation">,</span>\n            <span class="token punctuation">]</span>\n        <span class="token punctuation">}</span>\n    <span class="token punctuation">}</span><span class="token punctuation">,</span>\n<span class="token punctuation">]</span>\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br><span class="line-number">13</span><br><span class="line-number">14</span><br><span class="line-number">15</span><br><span class="line-number">16</span><br><span class="line-number">17</span><br><span class="line-number">18</span><br><span class="line-number">19</span><br><span class="line-number">20</span><br><span class="line-number">21</span><br><span class="line-number">22</span><br></div></div><h3 id="内置更多的快速正则校验"><a class="header-anchor" href="#内置更多的快速正则校验">#</a> 内置更多的快速正则校验</h3><ul><li>data_format.numeric 数字型字符串</li><li>email 邮箱</li><li>data_format.chinese 中文</li><li>data_format.url url格式</li><li>data_format.cellphone 手机号码</li><li>data_format.idcard 身份证号码</li></ul><h3 id="data-format-dataexpansion-自定义数据类型"><a class="header-anchor" href="#data-format-dataexpansion-自定义数据类型">#</a> data_format.DataExpansion 自定义数据类型</h3><div class="language-python ext-py line-numbers-mode"><pre class="language-python"><code><span class="token keyword">from</span> api_shop<span class="token punctuation">.</span>data_format <span class="token keyword">import</span> DataExpansion\n<span class="token keyword">from</span> datetime <span class="token keyword">import</span> datetime <span class="token keyword">as</span> dt\n\n<span class="token keyword">class</span> <span class="token class-name">datetime</span><span class="token punctuation">(</span><span class="token builtin">object</span><span class="token punctuation">,</span>metaclass<span class="token operator">=</span>DataExpansion<span class="token punctuation">)</span><span class="token punctuation">:</span>\n    <span class="token triple-quoted-string string">&#39;&#39;&#39;将str转换成datetime格式&#39;&#39;&#39;</span>\n    \n    class_name <span class="token operator">=</span> <span class="token string">&quot;&lt;class &#39;data_format.datetime&#39;&gt;&quot;</span>\n\n    <span class="token keyword">def</span> <span class="token function">__new__</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> string<span class="token punctuation">)</span><span class="token punctuation">:</span>\n        <span class="token keyword">if</span> <span class="token string">&#39;:&#39;</span> <span class="token keyword">in</span> string<span class="token punctuation">:</span>\n            <span class="token keyword">return</span> dt<span class="token punctuation">.</span>strptime<span class="token punctuation">(</span>string<span class="token punctuation">,</span> <span class="token string">&#39;%Y-%m-%d %H:%M:%S&#39;</span><span class="token punctuation">)</span>\n        <span class="token keyword">else</span><span class="token punctuation">:</span>\n            <span class="token keyword">return</span> dt<span class="token punctuation">.</span>strptime<span class="token punctuation">(</span>string<span class="token punctuation">,</span> <span class="token string">&#39;%Y-%m-%d&#39;</span><span class="token punctuation">)</span>\n</code></pre><div class="line-numbers"><span class="line-number">1</span><br><span class="line-number">2</span><br><span class="line-number">3</span><br><span class="line-number">4</span><br><span class="line-number">5</span><br><span class="line-number">6</span><br><span class="line-number">7</span><br><span class="line-number">8</span><br><span class="line-number">9</span><br><span class="line-number">10</span><br><span class="line-number">11</span><br><span class="line-number">12</span><br><span class="line-number">13</span><br></div></div><div class="custom-container tip"><p class="custom-container-title">TIP</p><p>继承的时候请按照上面的写法，继承为元类，并直接用__new__方法来返回一个全新的格式</p></div>',13),p={render:function(n,s){return t}}}}]);