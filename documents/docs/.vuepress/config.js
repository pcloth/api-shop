module.exports = {
    base: '/api-shop/',
    // dest: '../docs',
    head: [
        // 添加百度统计
        [
            "script",
            {},
            `var _hmt = _hmt || [];
            (function() {
                var hm = document.createElement("script");
                hm.src = "https://hm.baidu.com/hm.js?55405a77e01b4d671e84dd45880905a2";
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(hm, s);
            })();`
        ]
    ],
    lang: 'zh-CN',
    title: 'Api-Shop',
    description: '一个快速易用的restful-api接口工具包，兼容：django / flask / bottle。',
    themeConfig: {
        repo: 'pcloth/api-shop',
        logo: 'https://pcloth.gitee.io/api-shop/logo.png',
        contributors: false,
        navbar: [
            { text: '首页', link: '/' },
            { text: '介绍', link: '/introduction/' },
            { text: '快速上手', link: '/start/' },
            {
                text: '组件', children: [
                    '/components/ApiShop.md',
                    '/components/SingleApiShop.md',
                    '/components/Api.md',
                    '/components/func.md',
                    '/components/data_format.md',
                ]
            },
        ]
    },
}