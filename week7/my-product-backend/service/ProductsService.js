'use strict';

// 1. Import Model mà chúng ta đã tạo
const ProductModel = require('../models/ProductModel');

/**
 * Tạo sản phẩm mới (POST /products)
 *
 * body ProductInput Đối tượng ProductInput từ request
 * returns Product
 **/
exports.createProduct = async function(body) {
  try {
    // Dùng Mongoose 'create' để tạo sản phẩm mới từ 'body'
    const newProduct = await ProductModel.create(body);
    return newProduct.toJSON(); // Trả về đối tượng JSON (đã biến _id thành id)
  } catch (error) {
    console.error(error);
    // Nếu lỗi (ví dụ: thiếu 'name' hoặc 'price'), ném lỗi 400
    throw { status: 400, message: error.message };
  }
}

/**
 * Xóa sản phẩm (DELETE /products/{id})
 *
 * id String ID của sản phẩm
 * no response value expected
 **/
exports.deleteProduct = async function(id) {
  try {
    const deletedProduct = await ProductModel.findByIdAndDelete(id);
    if (!deletedProduct) {
      // Nếu không tìm thấy sản phẩm để xóa, ném lỗi 404
      throw { status: 404, message: 'Product not found' };
    }
    // DELETE thành công (HTTP 204) không cần trả về nội dung
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      throw { status: 400, message: 'Invalid Product ID format' };
    }
    throw error;
  }
}

/**
 * Lấy chi tiết sản phẩm theo ID (GET /products/{id})
 *
 * id String ID của sản phẩm
 * returns Product
 **/
exports.getProductById = async function(id) {
  try {
    const product = await ProductModel.findById(id);
    if (!product) {
      // Nếu không tìm thấy, ném lỗi 404
      throw { status: 404, message: 'Product not found' };
    }
    return product.toJSON();
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      throw { status: 400, message: 'Invalid Product ID format' };
    }
    throw error;
  }
}

/**
 * Lấy danh sách sản phẩm (GET /products)
 *
 * returns List
 **/
exports.getProducts = async function() {
  try {
    // 'find({})' để lấy tất cả sản phẩm
    const products = await ProductModel.find({});
    return products.map(p => p.toJSON()); // Trả về một mảng
  } catch (error) {
    console.error(error);
    throw { status: 500, message: error.message };
  }
}

/**
 * Cập nhật một phần thông tin sản phẩm (PATCH /products/{id})
 * (Dùng schema ProductUpdate)
 *
 * body ProductUpdate
 * id String ID của sản phẩm
 * returns Product
 **/
exports.partialUpdateProduct = async function(body, id) {
  try {
    // { new: true } để Mongoose trả về tài liệu *sau* khi đã cập nhật
    const updatedProduct = await ProductModel.findByIdAndUpdate(id, body, { new: true, runValidators: true });
    if (!updatedProduct) {
      throw { status: 404, message: 'Product not found' };
    }
    return updatedProduct.toJSON();
  } catch (error)
  {
    console.error(error);
    if (error.kind === 'ObjectId') {
      throw { status: 400, message: 'Invalid Product ID format' };
    }
    throw error;
  }
}

/**
 * Cập nhật toàn bộ thông tin sản phẩm (PUT /products/{id})
 * (Dùng schema ProductInput)
 *
 * body ProductInput
 * id String ID của sản phẩm
 * returns Product
 **/
exports.updateProduct = async function(body, id) {
  try {
    // 'overwrite: true' là mấu chốt của PUT: nó sẽ XÓA các trường cũ
    // và thay thế bằng 'body' mới.
    // runValidators: true để đảm bảo 'name' và 'price' vẫn có mặt
    const updatedProduct = await ProductModel.findByIdAndUpdate(id, body, { new: true, overwrite: true, runValidators: true });

    if (!updatedProduct) {
      throw { status: 404, message: 'Product not found' };
    }
    return updatedProduct.toJSON();
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      throw { status: 400, message: 'Invalid Product ID format' };
    }
    throw error;
  }
}