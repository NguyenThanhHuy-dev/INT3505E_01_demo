const mongoose = require('mongoose');

// Schema này định nghĩa cấu trúc của document trong MongoDB
// Nó nên khớp với các schema trong OpenAPI
const ProductSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
    },
    price: {
      type: Number,
      required: true,
    },
    description: {
      type: String,
      required: false, // Giống trong OpenAPI, description là không bắt buộc
    },
  },
  {
    timestamps: true, // Tự động thêm createdAt và updatedAt
    versionKey: false, // Không thêm trường __v (version)

    // Tùy chọn này rất quan trọng
    // Nó tự động biến _id (của Mongo) thành id (của OpenAPI)
    // và xóa _id khi trả về JSON
    toJSON: {
      virtuals: true,
      transform(doc, ret) {
        ret.id = ret._id;
        delete ret._id;
      },
    },
  }
);

module.exports = mongoose.model('Product', ProductSchema);
