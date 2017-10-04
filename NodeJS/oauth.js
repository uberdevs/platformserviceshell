var ids = {
    facebook: {
        clientID: process.env.facebookClientID,
        clientSecret: process.env.facebookClientSecret,
        callbackURL: process.env.facebookCallbackURL
    },
    twitter: {
        consumerKey: 'get_your_own',
        consumerSecret: 'get_your_own',
        callbackURL: "http://127.0.0.1:1337/auth/twitter/callback"
    },
    github: {
        clientID: 'get_your_own',
        clientSecret: 'get_your_own',
        callbackURL: "http://127.0.0.1:1337/auth/github/callback"
    },
    google: {
        clientID: 'get_your_own',
        clientSecret: 'get_your_own',
        callbackURL: 'http://127.0.0.1:1337/auth/google/callback'
    },
    instagram: {
        clientID: 'get_your_own',
        clientSecret: 'get_your_own',
        callbackURL: 'http://127.0.0.1:1337/auth/instagram/callback'
    }
};

module.exports = ids;
