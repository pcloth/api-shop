module.exports = {
    base: '/api-shop/',
    dest: '../docs',
    title: 'api-shop',
    description: '一个易用的、快速的restful-api接口工具包，兼容：django / flask / bottle。',
    locales: {
        '/': {
            lang: 'zh-CN',
            title: 'api-shop',
            description: '一个易用的、快速的restful-api接口工具包，兼容：django / flask / bottle。',

        },
        '/en/': {
            lang: 'en-US',
            title: 'api-shop',
            description: 'api-shop: An easy-to-use, fast restful-api interface toolkit compatible with django / flask / bottle.',
        }
    },
    themeConfig: {
        lastUpdated: 'Last Updated',
        search: true,
        searchMaxSuggestions: 10,
        locales: {
            '/': {
                selectText: 'Languages',
                label: '简体中文',
                editLinkText: '在 GitHub 上编辑此页',
                serviceWorker: {
                    updatePopup: {
                        message: "发现新内容可用.",
                        buttonText: "刷新"
                    }
                },
                algolia: {},
                nav: [
                    { text: '首页', link: '/' },
                    { text: '源码', link: 'https://github.com/pcloth/api-shop' },
                ],
                sidebar: [
                    '/',
                    '/update/',
                    '/start/',
                    '/components/',
                    '/docs/',
                ]
            },
            '/en/': {
                selectText: 'Languages',
                label: 'English',
                editLinkText: 'Edit this page on GitHub',
                serviceWorker: {
                    updatePopup: {
                        message: "New content is available.",
                        buttonText: "Refresh"
                    }
                },
                algolia: {},
                nav: [
                    { text: 'Home', link: '/en/' },
                    { text: 'Github', link: 'https://github.com/pcloth/api-shop' },
                ],
                sidebar: [
                    '/en/',
                    '/en/update/',
                    '/en/start/',
                    '/en/components/',
                    '/en/docs/',
                ]

            }
        },


    },
    plugins: {'baidu-tongji': {
        hm: '55405a77e01b4d671e84dd45880905a2'
      }}
}