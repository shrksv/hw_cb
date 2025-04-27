from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from PIL import Image
import numpy as np
import os

input_image_path   = "images/input.png"
signed_image_path  = "images/signed_image.png"
private_key_path   = "keys/private.pem"
SIGNATURE_SIZE     = 512 

def load_private_key(path):
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

def sign_data(private_key, data: bytes) -> bytes:
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def hide_data_in_image(image_array: np.ndarray, data_bytes: bytes) -> np.ndarray:
    flat = image_array.flatten()
    bits = np.unpackbits(np.frombuffer(data_bytes, dtype=np.uint8))
    n_bits = bits.size

    flat[:n_bits] &= 0xFE
    flat[:n_bits] |= bits

    return flat.reshape(image_array.shape)

def main():
    os.makedirs("images", exist_ok=True)

    img = Image.open(input_image_path).convert("RGB")
    arr = np.array(img)

    flat = arr.flatten().copy()
    total_bits = SIGNATURE_SIZE * 8
    flat[:total_bits] &= 0xFE
    clean_arr = flat.reshape(arr.shape)

    digest = hashes.Hash(hashes.SHA256())
    digest.update(clean_arr.tobytes())
    image_hash = digest.finalize()

    private_key = load_private_key(private_key_path)
    signature = sign_data(private_key, image_hash)

    signed_arr = hide_data_in_image(arr, signature)

    signed_img = Image.fromarray(signed_arr)
    signed_img.save(signed_image_path)

if __name__ == "__main__":
    main()
