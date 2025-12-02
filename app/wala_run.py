import os
import subprocess
import base64

wala_home = ("models/WaLa/")
gen_home = wala_home + "examples/text/"
conda_home = '/home/jared/miniconda3/bin/conda'


terminal_messages = [
    "Test",
    "GENERATING DEPTH MAPS...",
    "RENAMING FILES...",
    "GENERATING 3D MODEL"
]
# global commands
commands = [
    ['mv', gen_home + 'depth_maps/image_0.png', gen_home + 'depth_maps/3.png'],
    ['mv', gen_home + 'depth_maps/image_1.png', gen_home + 'depth_maps/6.png'],
    ['mv', gen_home + 'depth_maps/image_2.png', gen_home + 'depth_maps/10.png'],
    ['mv', gen_home + 'depth_maps/image_3.png', gen_home + 'depth_maps/26.png'],
    ['mv', gen_home + 'depth_maps/image_4.png', gen_home + 'depth_maps/49.png'],
    ['mv', gen_home + 'depth_maps/image_5.png', gen_home + 'depth_maps/50.png'],

    [conda_home, 'run', '-n', 'wala', 
    'python3', wala_home + 'run.py', 
        '--model_name', 'ADSKAILab/WaLa-DM6-1B', 
        '--dm6', 
        gen_home + 'depth_maps/3.png',
        gen_home + 'depth_maps/6.png',
        gen_home + 'depth_maps/10.png',
        gen_home + 'depth_maps/26.png',
        gen_home + 'depth_maps/49.png',
        gen_home + 'depth_maps/50.png', 
        '--output_dir', gen_home,
        '--output_format', 'obj',
        '--scale', '1.5',
        '--diffusion_rescale_timestep', '10']
]

def serialize_model(path_to_model):
    # path_to_model = gen_home + '3/3.obj'
    with open(path_to_model, "rb") as f:
        obj_bytes = f.read()
        obj_b64 = base64.b64encode(obj_bytes).decode('utf-8') # Encode to base64 string for safe JSON transport
    encoded_size = len(obj_b64.encode("utf-8"))
    print(f"Encoded size: {encoded_size} bytes")
    payload = {
        "filename": "3.obj",
        "data": obj_b64
    }
    print("MODEL SUCCESSFULLY ENCODED!!!\n\n\n")
    return payload

def generate_model(prompt):
    # global commands
    gen_cmd = [conda_home, 'run', '-n', 'wala', 
                'python3', wala_home + 'run.py', 
                '--model_name', 'ADSKAILab/WaLa-MVDream-DM6', 
                '--text_to_dm6', f'\"{prompt}\"', 
                '--output_dir', gen_home]
    commands.insert(0, gen_cmd)
    print(f"COMMANDS LENGTH: {len(commands)}\n\n")
    for i in range(len(commands)):
        # Run each command in WSL, in the target directory
        # cmd = ['wsl'] + commands[i]
        cmd = commands[i]
        # print(terminal_messages[i])
        # print(cmd)
        print(f"Running: {cmd}\n\n")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding = 'utf-8'
        )
        print(result.stdout)
        print("STDERR:", result.stderr)
    path_to_model = wala_home + '/examples/text/3/3.obj'
    print("FINISHED GENERATING MODEL TO: " + path_to_model)
    # commands = commands[1:]
    commands.pop(0)
    return path_to_model


def main(prompt):
    path_to_model = generate_model(prompt)
    
    # path_to_model = gen_home + '3/3.obj'
#    path_to_model = r'\\wsl.localhost\Ubuntu\home\jared\documents\phd\distributed_computing\WaLa\examples\text\3\3.obj'
    path_to_model = wala_home + '/examples/text/3/3.obj'
    payload = serialize_model(path_to_model)
    return payload

# main("prompt")
