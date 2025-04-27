from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from PIL import Image
import numpy as np


signed_image_path = "images/signed_image.png"
public_key_path   = "keys/public.pem"
SIGNATURE_SIZE    = 512

def load_public_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def extract_data_from_image(image_array: np.ndarray, num_bytes: int) -> bytes:
    flat = image_array.flatten()
    total_bits = num_bytes * 8
    bits = flat[:total_bits] & 1
    return np.packbits(bits).tobytes()

def main():
    img = Image.open(signed_image_path).convert("RGB")
    arr = np.array(img)

    signature = extract_data_from_image(arr, SIGNATURE_SIZE)
    flat = arr.flatten().copy()
    total_bits = SIGNATURE_SIZE * 8
    flat[:total_bits] &= 0xFE
    clean_arr = flat.reshape(arr.shape)

    digest = hashes.Hash(hashes.SHA256())
    digest.update(clean_arr.tobytes())
    image_hash = digest.finalize()

    public_key = load_public_key(public_key_path)
    try:
        public_key.verify(
            signature,
            image_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Correct")
    except InvalidSignature:
        print("Not correct")

if __name__ == "__main__":
    main()
