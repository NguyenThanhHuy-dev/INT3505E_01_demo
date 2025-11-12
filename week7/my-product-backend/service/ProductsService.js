'use strict';

const ProductModel = require('../models/ProductModel');

exports.createProduct = async function(body) {
  try {
    const newProduct = await ProductModel.create(body);
    return newProduct.toJSON(); // Trả về đối tượng JSON (đã biến _id thành id)
  } catch (error) {
    console.error(error);
    // Nếu lỗi (ví dụ: thiếu 'name' hoặc 'price'), ném lỗi 400
    throw { status: 400, message: error.message };
  }
}


exports.deleteProduct = async function(id) {
  try {
    const deletedProduct = await ProductModel.findByIdAndDelete(id);
    if (!deletedProduct) {
      throw { status: 404, message: 'Product not found' };
    }
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      throw { status: 400, message: 'Invalid Product ID format' };
    }
    throw error;
  }
}

exports.getProductById = async function(id) {
  try {
    const product = await ProductModel.findById(id);
    if (!product) {
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

exports.getProducts = async function() {
  try {
    const products = await ProductModel.find({});
    return products.map(p => p.toJSON());
  } catch (error) {
    console.error(error);
    throw { status: 500, message: error.message };
  }
}

exports.partialUpdateProduct = async function(body, id) {
  try {
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

exports.updateProduct = async function(body, id) {
  try {
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