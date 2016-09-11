var webpack = require('webpack');
var apiHost = "'http://api.bilalkhan.tech'";


module.exports = {
   entry: './js/app.js',
	
   output: {
      path:__dirname,
      filename: './static/bundle.js',
   },
   plugins: [
      new webpack.optimize.UglifyJsPlugin(),
      new webpack.DefinePlugin({
         __API__: apiHost,
         'process.env':{
            'NODE_ENV': JSON.stringify('production')
         }
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
