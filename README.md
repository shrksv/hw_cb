Digital Signature for Image
Project Overview
This project demonstrates how to digitally sign an image using an RSA private key and later verify that signature with a public key.
It ensures that an image has not been modified and confirms the author's authenticity.
Project Structure
├── images/
│   ├── image.png        
│   └── image.sig        
├── keys/
│   ├── private.pem     
│   └── public.pem       
├── sign_image.py        
├── verify_image.py      
How to Use
1. Generate RSA Keys (external step) Key generation is in generate_keys.py
2. Sign an ImageMake sure you have:
keys/private.pem
images/image.png
Then run:
python sign_image.py
This will create a signature file:
images/image.sig3.
Verify an ImageMake sure you have:
keys/public.pem
images/image.png
images/signed_image.png
Then run:
python verify_image.py
Expected output:
Correct
Not correct
Scripts Details:
sign_image.pyLoads the RSA private key.
Reads the image file.
Generates a PSS-SHA256 based signature.
Saves the signature into images/signed_image.png
verify_image.py
Loads the RSA public key.
Reads the image file and the signature.
Verifies that the signature matches the image using PSS-SHA256.
Outputs validation result.

The project assumes fixed filenames: image.png and image.sig.
