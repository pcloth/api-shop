import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { defineUserConfig } from 'vuepress'

export default defineUserConfig({
    base: '/api-shop/',
    bundler: viteBundler(),
    head: [
        [
            'script',
            {},
            `var _hmt = _hmt || [];
            (function() {
                var hm = document.createElement("script");
                hm.src = "https://hm.baidu.com/hm.js?55405a77e01b4d671e84dd45880905a2";
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(hm, s);
            })();`,
        ],
    ],
    lang: 'zh-CN',
    title: 'Api-Shop',
    description: '框架无关、类型驱动的 Python API 契约与调度器。',
    theme: defaultTheme({
        repo: 'pcloth/api-shop',
        logo: '/logo.png',
        contributors: false,
        navbar: [
            { text: '首页', link: '/' },
            { text: '介绍', link: '/introduction/' },
            { text: '快速上手', link: '/start/' },
            { text: '从 1.x 升级', link: '/migration/' },
            {
                text: '指南',
                children: [
                    '/components/ApiShop.md',
                    '/components/SingleApiShop.md',
                    '/components/Api.md',
                    '/components/func.md',
                    '/components/data_format.md',
                ],
            },
        ],
    }),
})
