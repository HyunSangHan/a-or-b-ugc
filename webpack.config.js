const path = require("path");
const webpack = require("webpack");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  mode: "development",
  entry: [
    "./feedpage/static/feedpage/accounts.js",
    "./feedpage/static/feedpage/feeds.js",
    "./feedpage/static/feedpage/common.scss"
  ],
  output: {
    filename: "index.js",
    path: path.resolve("./feedpage/static/dist")
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
        exclude: /node_modules/
      },
      // {
      //   test: /\.(png|jpg)$/,
      //   loader: "file-loader",
      //   options: {
      //     publicPath: "./dist/",
      //     name: "[name].[ext]?[hash]"
      //   }
      // },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: "babel-loader"
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new webpack.BannerPlugin({
      banner: `Built at: ${new Date().toLocaleString()}`
    }),
    new MiniCssExtractPlugin({ filename: "common.css" })
  ]
};
