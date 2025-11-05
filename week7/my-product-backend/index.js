'use strict';

// === THÊM PHẦN NÀY VÀO ĐẦU FILE ===
const mongoose = require('mongoose');

// Vì bạn đang dùng MongoDB local đã cài
// Đây là chuỗi kết nối (Connection String) của bạn.
// 'product_db' là tên database, nó sẽ tự động được tạo.
const MONGO_URI = 'mongodb://localhost:27017/product_db';

mongoose.connect(MONGO_URI)
  .then(() => console.log('✅ Connected to MongoDB successfully!'))
  .catch((err) => console.error('❌ Could not connect to MongoDB:', err));

var path = require('path');
var http = require('http');

var oas3Tools = require('oas3-tools');
var serverPort = 3000;

// swaggerRouter configuration
var options = {
    routing: {
        controllers: path.join(__dirname, './controllers')
    },
};

var expressAppConfig = oas3Tools.expressAppConfig(path.join(__dirname, 'api/openapi.yaml'), options);
var app = expressAppConfig.getApp();

// Initialize the Swagger middleware
http.createServer(app).listen(serverPort, function () {
    console.log('Your server is listening on port %d (http://localhost:%d)', serverPort, serverPort);
    console.log('Swagger-ui is available on http://localhost:%d/docs', serverPort);
});

