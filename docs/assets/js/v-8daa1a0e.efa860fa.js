(self.webpackChunkdocuments=self.webpackChunkdocuments||[]).push([[509],{6464:(e,i,t)=>{"use strict";t.r(i),t.d(i,{data:()=>l});const l={key:"v-8daa1a0e",path:"/",title:"",lang:"zh-CN",frontmatter:{home:!0,heroImage:"/logo.png",description:"这是一个Api控制模组，让你快速开始业务代码。",actions:[{text:"了解Api-shop →",link:"/introduction/",type:"primary"}],features:[{title:"简洁",details:"用一个json数据或者@add_api装饰器配置接口"},{title:"自动",details:"自动校验参数、自动转换参数格式、自动生成文档和mock工具"},{title:"省时",details:"简化业务代码，外部和内部均可复用。一切只为少加班。"}],footer:"MIT Licensed | Copyright © 2019-2021 Pcloth"},excerpt:"",headers:[{level:2,title:"核心功能：",slug:"核心功能",children:[]}],filePathRelative:"README.md",git:{updatedTime:1624611183e3}}},2380:(e,i,t)=>{"use strict";t.r(i),t.d(i,{default:()=>o});const l=(0,t(6252).uE)('<p><img src="https://img.shields.io/pypi/v/api-shop?logo=api-shop" alt="PyPI"> <img src="https://img.shields.io/pypi/dm/api-shop" alt="PyPI - Downloads"></p><h2 id="核心功能"><a class="header-anchor" href="#核心功能">#</a> <strong>核心功能：</strong></h2><ol><li>配置化api生成。</li><li>自动校验request提交的数据，并转换成指定格式，支持：int，float，list，dict，set，tuple，bool</li><li>自动生成api文档，并提供一个web页面可供查询和mock数据演示。</li><li>兼容 <code>django</code> , <code>flask</code> , <code>bottle</code> (如果不指定框架，默认按这个顺序识别框架)</li><li>自动生成接口<code>骨架文件</code>功能beta（请谨慎开启）。</li><li>自定义格式转换器，data_format.datetime格式转换类；&#39;2019-01-18 23:25:25&#39; to datetime</li><li>支持正则格式校验。</li><li>多国语言支持，也支持自定义语言包。</li><li>文档热重载。</li><li>默认值支持方法函数。</li><li>支持url中包含参数，例如 <code>/api/user/&lt;id&gt;</code>，并且在配置methods参数的时候设置它的规则。</li><li>支持多url绑定一个接口</li><li>支持指定参数的可选项，例如：[1,4,7]，收到这个列表之外的参数就会触发bad_request</li><li>可以在代码中直接调用Api业务代码：<code>api_run</code>（将移除<code>get_api_result_json</code>和<code>get_api_result_response</code>）</li><li>支持在Api类中定义response_docs来制作返回值文档，并支持模型字段引入；以及模型部分字段引入类：ApiResponseModelFields</li></ol>',3),o={render:function(e,i){return l}}}}]);