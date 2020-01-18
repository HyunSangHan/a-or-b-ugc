const path = require("path");
const webpack = require("webpack");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
  mode: "development",
  entry: ["./feedpage/static/feedpage/accounts.js", "./feedpage/static/feedpage/feeds.js"],
  output: {
    filename: "index.js",
    path: path.resolve("./feedpage/static/dist")
  },
  module: {
    rules: [
      // {
      //   test: /\.css$/,
      //   use: ["style-loader", "css-loader"]
      // },
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
  ]
}
