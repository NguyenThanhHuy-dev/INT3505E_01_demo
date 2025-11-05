'use strict';


/**
 * Tạo sản phẩm mới
 *
 * body ProductInput 
 * returns Product
 **/
exports.createProduct = function(body) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = {
  "price" : 0.8008281904610115,
  "name" : "name",
  "description" : "description",
  "id" : "id"
};
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Xóa sản phẩm
 *
 * id String ID của sản phẩm
 * no response value expected for this operation
 **/
exports.deleteProduct = function(id) {
  return new Promise(function(resolve, reject) {
    resolve();
  });
}


/**
 * Lấy chi tiết sản phẩm theo ID
 *
 * id String ID của sản phẩm (Mongo ObjectId)
 * returns Product
 **/
exports.getProductById = function(id) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = {
  "price" : 0.8008281904610115,
  "name" : "name",
  "description" : "description",
  "id" : "id"
};
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Lấy danh sách sản phẩm
 *
 * returns List
 **/
exports.getProducts = function() {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ {
  "price" : 0.8008281904610115,
  "name" : "name",
  "description" : "description",
  "id" : "id"
}, {
  "price" : 0.8008281904610115,
  "name" : "name",
  "description" : "description",
  "id" : "id"
} ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Cập nhật một phần thông tin sản phẩm
 *
 * body ProductUpdate 
 * id String ID của sản phẩm
 * returns Product
 **/
exports.partialUpdateProduct = function(body,id) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = {
  "price" : 0.8008281904610115,
  "name" : "name",
  "description" : "description",
  "id" : "id"
};
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Cập nhật toàn bộ thông tin sản phẩm
 *
 * body ProductInput 
 * id String ID của sản phẩm
 * returns Product
 **/
exports.updateProduct = function(body,id) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = {
  "price" : 0.8008281904610115,
  "name" : "name",
  "description" : "description",
  "id" : "id"
};
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}

