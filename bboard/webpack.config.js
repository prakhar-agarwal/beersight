const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const merge = require('webpack-merge');
const validate = require('webpack-validator');
const webpack = require('webpack');
// const EnvironmentPlugin = require('webpack-env');

const PATHS = {
    app: path.join(__dirname, 'src'),
    build: path.join(__dirname, 'build')
};

const common = {
    entry: {
        app: [PATHS.app + '/components/index.js']
    },
    output: {
        path: PATHS.build,
        filename: '[name].js'
    },
    module: {
        loaders: [{
            test: /\.js?$/,
            include: [__dirname, 'src'],
            loader: 'babel-loader',
            query: {
                presets: ['es2015', 'react']
            }
        }, {
            test: /\.scss?$/,
            include: [__dirname, 'src'],
            loader: ExtractTextPlugin.extract('css!sass')
        }]
    },
    devServer: {
        port: 3000,
        historyApiFallback: true
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'SnapCards',
            template: 'src/index.html'
        }),
        new ExtractTextPlugin('style.css', {
            allChunks: true
        }),
        new CopyWebpackPlugin([
            { from: 'src/static', to: 'static' }
        ])
    ]
};


var config;

// Detect how npm is run and branch based on that
switch (process.env.npm_lifecycle_event) {
    case 'build':
        config = merge(common, {});
        break;
    default:
        config = merge(common, {
          plugins: [
            new webpack.DefinePlugin({
             'process.env':{
               'NODE_ENV': JSON.stringify('dev')
             }
           })
          ]
        });
}

module.exports = validate(config);
