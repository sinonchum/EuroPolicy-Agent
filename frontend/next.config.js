/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    // 由于 8G 内存，禁用一些重型编译选项
    swcMinify: true,
}

module.exports = nextConfig
