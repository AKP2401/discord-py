import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
print("Installing Discord.py...")
install('discord.py')
print('Discord.py installation complete\n\n')

print('Installing requests...')
install('requests')
print('Requests installation complete\n\n')

print('Installing PyNaCl...')
install('PyNaCl')
print('PyNaCl installation complete\n\n')

print('Installing python-dotenv...')
install('python-dotenv')
print('python-env isntallation complete\n\n')

print('Installing essential=generators...')
install('essential-generators')
print('essential-generators installation complete\n\n')