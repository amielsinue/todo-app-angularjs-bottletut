/**
 * Created by ayanez on 1/18/17.
 */
var path = require('path');
module.exports = {
    context: path.resolve('js'),
    entry: ['./index'],
    output: {
        path: path.resolve('js'),
        publicPath: '../../js',
        filename: 'app.min.js'
    },
    module:{
        loaders:[
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            }
        ]
    },
    resolve:{
        extentions: ['', '.js', '.es6']
    }
}