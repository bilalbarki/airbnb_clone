var webpack = require('webpack');
var apiHost = "'http://localhost:3333'";


module.exports = {
   entry: './js/app.js',
	
   output: {
      path:__dirname,
      filename: './static/bundle.js',
   },
   plugins: [
      new webpack.DefinePlugin({
         __API__: apiHost
      })
   ],
   module: {
      loaders: [
         {
            //test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
               presets: ['es2015', 'react']
            }
         }
      ]
   }
};
