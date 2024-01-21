import random
import numpy as np
from scipy.integrate import odeint

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = 'A' if char.isupper() else 'a'
            result += chr((ord(char) - ord(start) + shift) % 26 + ord(start))
        else:
            result += char
    return result

def lorenz_system(state, t, sigma, beta, rho):
    x, y, z = state
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z

def generate_lorenz_points(initial_state, n_points, sigma=10, beta=8/3, rho=28):
    t = np.linspace(0, 1, n_points * 10)  # Increased number of points for more precision
    points = odeint(lorenz_system, initial_state, t, args=(sigma, beta, rho))
    return points[::10]  # Downsample to get the required number of points

def lorenz_transposition_cipher(text, lorenz_points):
    sorted_indices = np.argsort(lorenz_points[:, 0])
    transposed_text = [''] * len(text)
    for original_index, sorted_index in enumerate(sorted_indices):
        if original_index < len(text):
            transposed_text[sorted_index] = text[original_index]
    return ''.join(transposed_text)



def generate_complex_cipher(text, initial_state):
    # Cuneiform-style symbol representations for each letter
    cuneiform_symbols = {
        'A': '𒀀', 'B': '𒀁', 'C': '𒀂', 'D': '𒀃', 'E': '𒀄',
        'F': '𒀅', 'G': '𒀆', 'H': '𒀇', 'I': '𒀈', 'J': '𒀉',
        'K': '𒀊', 'L': '𒀋', 'M': '𒀌', 'N': '𒀍', 'O': '𒀎',
        'P': '𒀏', 'Q': '𒀐', 'R': '𒀑', 'S': '𒀒', 'T': '𒀓',
        'U': '𒀔', 'V': '𒀕', 'W': '𒀖', 'X': '𒀗', 'Y': '𒀘', 
        'Z': '𒀙', 
        '0': '𒐀', '1': '𒐁', '2': '𒐂', '3': '𒐃', '4': '𒐄',
        '5': '𒐅', '6': '𒐆', '7': '𒐇', '8': '𒐈', '9': '𒐉',
        ' ': ' ', ',': ',','$','<'
    }


    shifted_text = caesar_cipher(text, 3)
    lorenz_points = generate_lorenz_points(initial_state, len(shifted_text))
    transposed_text = lorenz_transposition_cipher(shifted_text, lorenz_points)
    encoded_text = ''.join([cuneiform_symbols.get(char.upper(), char) for char in transposed_text])
    return encoded_text

def reverse_caesar_cipher(text, shift):
    return caesar_cipher(text, -shift)

def reverse_lorenz_transposition_cipher(transposed_text, lorenz_points):
    sorted_indices = np.argsort(lorenz_points[:, 0])
    original_text = [''] * len(transposed_text)
    for original_index, sorted_index in enumerate(sorted_indices):
        if sorted_index < len(transposed_text):
            original_text[original_index] = transposed_text[sorted_index]
    return ''.join(original_text)


def decipher_complex_cipher(encoded_text, initial_state):
    cuneiform_symbols = {
        'A': '𒀀', 'B': '𒀁', 'C': '𒀂', 'D': '𒀃', 'E': '𒀄',
        'F': '𒀅', 'G': '𒀆', 'H': '𒀇', 'I': '𒀈', 'J': '𒀉',
        'K': '𒀊', 'L': '𒀋', 'M': '𒀌', 'N': '𒀍', 'O': '𒀎',
        'P': '𒀏', 'Q': '𒀐', 'R': '𒀑', 'S': '𒀒', 'T': '𒀓',
        'U': '𒀔', 'V': '𒀕', 'W': '𒀖', 'X': '𒀗', 'Y': '𒀘', 
        'Z': '𒀙', 
        '0': '𒐀', '1': '𒐁', '2': '𒐂', '3': '𒐃', '4': '𒐄',
        '5': '𒐅', '6': '𒐆', '7': '𒐇', '8': '𒐈', '9': '𒐉',
        ' ': ' ', ',': ','
    }
    reversed_symbols = {v: k for k, v in cuneiform_symbols.items()}
    text_with_symbols = ''.join([reversed_symbols.get(char, char) for char in encoded_text])
    lorenz_points = generate_lorenz_points(initial_state, len(text_with_symbols))
    transposed_text = reverse_lorenz_transposition_cipher(text_with_symbols, lorenz_points)
    decrypted_text = reverse_caesar_cipher(transposed_text, 3)
    return decrypted_text




phrase = "THERE IS AN INVISIBLE PINK DRAGON IN MY GARAGE, AND YOU ALL BOUGHT IT."
initial_state = [1.0 ,3.02, 2.03] #initial state of lorenz system
ciphered_phrase = generate_complex_cipher(phrase, initial_state)
print(ciphered_phrase)

deciphered_phrase = decipher_complex_cipher(ciphered_phrase, initial_state)
print(f'deciphered:{deciphered_phrase}')
