let devMode = process.env.NODE_ENV === 'development';

if (devMode) {
  module.exports = {
    api_url: "http://localhost:6543/api/search"
  };
} else {
  module.exports = {
    api_url: "http://localhost:6543/api/search"
  };
}

