module.exports = {
    title: 'api-shop',
    description: '一个易用的、快速的restful-api接口工具包，兼容：`django` / `flask` / `bottle`。',

    locales: {
        '/': {
            lang: 'zh-CN',
            title: 'api-shop',
            description: '一个易用的、快速的restful-api接口工具包，兼容：`django` / `flask` / `bottle`。'
        },
        '/en/': {
            lang: 'en-US',
            title: 'api-shop',
            description: 'api-shop: An easy-to-use, fast restful-api interface toolkit compatible with `django` / `flask` / `bottle`.'

        }
    },
    themeConfig: {
        lastUpdated: 'Last Updated',
        search: true,
        searchMaxSuggestions: 10,
        nav: [
            { text: 'Home', link: '/' },
            { text: 'Github', link: 'https://github.com/pcloth/api-shop' },
        ],
        sidebar: [
            '/',
            '/update/',
            '/start/',
            '/components/'
        ]
    },
}