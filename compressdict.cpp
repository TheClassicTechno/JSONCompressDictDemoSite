#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "brotli/c/include/brotli/encode.h"

std::vector<uint8_t> read_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    return std::vector<uint8_t>((std::istreambuf_iterator<char>(file)),
                                 std::istreambuf_iterator<char>());
}

void write_file(const std::string& filename, const std::vector<uint8_t>& data) {
    std::ofstream file(filename, std::ios::binary);
    file.write(reinterpret_cast<const char*>(data.data()), data.size());
}

int main() {
    std::vector<uint8_t> input = read_file("delta.json");
    std::vector<uint8_t> dictionary = read_file("base.json");
    std::vector<uint8_t> output(input.size()); // Overestimate output buffer size

    size_t encoded_size = output.size();
    BrotliEncoderState* s = BrotliEncoderCreateInstance(nullptr, nullptr, nullptr);
    BrotliEncoderSetParameter(s, BROTLI_PARAM_QUALITY, 11);
    BrotliEncoderSetParameter(s, BROTLI_PARAM_LGWIN, 22);
    BrotliEncoderSetCustomDictionary(s, dictionary.size(), dictionary.data());

    bool ok = BrotliEncoderCompress(s, BROTLI_OPERATION_FINISH,
                                    &encoded_size, output.data(),
                                    input.size(), input.data());
    BrotliEncoderDestroyInstance(s);

    if (!ok) {
        std::cerr << "Compression failed!" << std::endl;
        return 1;
    }

    output.resize(encoded_size);
    write_file("delta.json.br", output);
    std::cout << "Compressed delta.json.br using base.json as dictionary." << std::endl;
    return 0;
}
