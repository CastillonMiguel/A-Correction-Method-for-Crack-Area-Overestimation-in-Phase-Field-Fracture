r"""
.. _ref_skeleton_3d:

Skeletonization — crack area measurement from 3D AT2 simulation
---------------------------------------------------------------

This script measures the crack area from the phase-field VTU output of
:ref:`ref_central_cracked_3d_simulation_at2` using a 2D image-processing pipeline.
The resulting crack area is used as the **Skeleton** reference correction method in the
3D benchmark (see :ref:`ref_examples_phase_field_central_crack_3d`).

**Workflow**

1. Render each VTU file to a PNG image (front :math:`xy`-plane view), marking regions
   with :math:`\phi > 0.95` in red on a black specimen background.
2. Auto-detect the specimen bounding box in pixel space to compute scale factors
   :math:`d_x` (mm/pixel) and :math:`d_y` (mm/pixel).
3. Apply HSV-based red-detection to isolate crack pixels from the background.
4. Skeletonize the binary crack mask (``skimage.morphology.skeletonize``) and extract
   physical :math:`(x, y)` coordinates of the centerline.
5. Fit a smoothing spline through the skeleton points to obtain a sub-pixel crack path.
6. Measure the arc length of the spline → crack length in mm.
7. Multiply by specimen thickness :math:`t = 0.05` mm → crack **area** in mm².
8. Extract simulation times from the PVD file, interpolate crack lengths to a uniform
   step-time grid, and save the result.

**Output files** (written to ``results_simulation_3d/crack_measurement/``)

- ``crack_lengths.txt`` — raw spline arc lengths (mm) per time step.
- ``step_time_crack_length.txt`` — (simulation time, crack length) pairs.
- ``interpolated_step_time_crack_length.txt`` — crack length interpolated to integer
  step indices; read by :ref:`ref_central_cracked_3d_simulation_at2` to compute
  :math:`\mathcal{F}_\mathrm{skeleton}`.
"""

import os
import pyvista as pv
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

# import imageio.v2 as imageio
# from skimage.morphology import skeletonize
# from skimage.color import rgb2hsv
# from scipy.interpolate import splprep, splev

# import xml.etree.ElementTree as ET


# def extract_steps_and_times_from_pvd(pvd_path, output_txt_path):
#     """
#     Extracts step indices and simulation times from a .pvd file and saves them to a text file.
#     """
#     tree = ET.parse(pvd_path)
#     root = tree.getroot()
#     collection = root.find('Collection')
#     if collection is None:
#         print("No <Collection> found in PVD file.")
#         return

#     steps = []
#     times = []
#     for idx, dataset in enumerate(collection.findall('DataSet')):
#         time = float(dataset.attrib.get('timestep', '0'))
#         steps.append(idx)
#         times.append(time)

#     data = np.column_stack((steps, times))
#     np.savetxt(output_txt_path, data, header="step time", fmt='%d %.8f', comments='')
    


# def create_gif_from_images(folder, output_gif, duration=1.0):
#     """
#     Creates a GIF from a sequence of images in a specified folder.

#     Parameters:
#     - folder (str): Path to the folder containing the images.
#     - output_gif (str): Path to save the output GIF.
#     - duration (float): Duration for each frame in the GIF (in seconds).
#     """
#     # Get all image files (e.g., PNG, JPG) and sort them
#     images = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

#     frames = []
#     for fname in images:
#         img = imageio.imread(os.path.join(folder, fname))
#         # Convert to uint8 if needed
#         if img.dtype != 'uint8':
#             img = (img * 255).astype('uint8')
#         # Remove alpha channel if present
#         if img.ndim == 3 and img.shape[-1] == 4:
#             img = img[..., :3]
#         frames.append(img)

#     imageio.mimsave(output_gif, frames, duration=duration)
#     print(f"GIF saved as {output_gif}")
    
    
# def get_black_bbox(image):
#     """
#     Returns the bounding box (min_row, max_row, min_col, max_col) of the black region in a grayscale or RGB image.
#     """
#     # If RGB, convert to grayscale
#     if image.ndim == 3:
#         gray = np.mean(image[..., :3], axis=2)
#     else:
#         gray = image
#     # Black threshold (tune if needed)
#     black_mask = gray < 0.2
#     rows = np.any(black_mask, axis=1)
#     cols = np.any(black_mask, axis=0)
#     min_row, max_row = np.where(rows)[0][[0, -1]]
#     min_col, max_col = np.where(cols)[0][[0, -1]]
#     return min_row, max_row, min_col, max_col


# def generate_crack_images(input_folder, output_folder, threshold, ratio_horizontal_div_vertical, with_spline=False):
#     """
#     Generates PNG images from .vtu files, highlighting the crack region in red.
#     """
#     os.makedirs(output_folder, exist_ok=True)
#     pv.global_theme.allow_empty_mesh = True
#     x0 = -0.5
#     y0 = -3.0
#     # List all .pvtu files
#     pvtu_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.vtu')])[0:]

#     for fname in pvtu_files:
#         file_path = os.path.join(input_folder, fname)
#         file_vtu = pv.read(file_path)
   
#         if threshold is not None:
#             crack = file_vtu.threshold(value=threshold, scalars='phi', invert=False)

#             plotter = pv.Plotter(off_screen=True)
#             plotter.set_background('white') 

#             plotter.add_mesh(file_vtu, color='black')    # <-- Optional: ensure it matches face color)
#             plotter.add_mesh(crack, color='red')

#             plotter.camera_position = 'xy'
#             img_path = os.path.join(output_folder, fname.replace('.vtu', '.png'))
#             plotter.show(auto_close=False, window_size=(int(2048*ratio_horizontal_div_vertical), 2048), interactive=False)
#             plotter.enable_anti_aliasing('ssaa')  # Super-sample anti-aliasing for smoother lines
#             plotter.screenshot(img_path, transparent_background=True)
#             plotter.close()
#             del file_vtu, crack, plotter  # Free memory
    
#         elif with_spline:
#             plotter = pv.Plotter(off_screen=True)
#             plotter.set_background('white')

#             plotter.add_mesh(file_vtu, scalars='phi', show_scalar_bar=False)  # Plot the 'phi' scalar

#             # Overlay spline line if available
#             spline_folder = os.path.join(os.path.dirname(output_folder), "spline_coordinates")
#             spline_file = os.path.join(spline_folder, fname.replace('.vtu', '_spline.txt'))
#             if os.path.exists(spline_file):
#                 data = np.loadtxt(spline_file, skiprows=1)
#                 if data.size > 0:
#                     if data.ndim == 1:
#                         data = data[None, :]
#                     x_spline, y_spline = data[:, 0], data[:, 1]
#                     x_spline += x0
#                     y_spline += y0
#                     # y_spline = -(y_spline)
#                     line_points_spline = np.column_stack((x_spline, y_spline, np.zeros_like(x_spline)+0.05))
#                     line_spline = pv.lines_from_points(line_points_spline)
#                     plotter.add_mesh(line_spline, color='red', line_width=5)

#             plotter.camera_position = 'xy'
#             img_path = os.path.join(output_folder, fname.replace('.vtu', '.png'))
#             plotter.show(auto_close=False, window_size=(int(2048*ratio_horizontal_div_vertical), 2048), interactive=False)
#             plotter.enable_anti_aliasing('ssaa')  # Super-sample anti-aliasing for smoother lines
#             plotter.screenshot(img_path, transparent_background=True)
#             plotter.close()
#             del file_vtu, plotter  # Free memory
            
#         else:
#             plotter = pv.Plotter(off_screen=True)
#             plotter.set_background('white')

#             plotter.add_mesh(file_vtu, scalars='phi', show_scalar_bar=False)  # Plot the 'phi' scalar
        
#             plotter.camera_position = 'xy'
#             img_path = os.path.join(output_folder, fname.replace('.vtu', '.png'))
#             plotter.show(auto_close=False, window_size=(int(2048*ratio_horizontal_div_vertical), 2048), interactive=False)
#             plotter.enable_anti_aliasing('ssaa')  # Super-sample anti-aliasing for smoother lines
#             plotter.screenshot(img_path, transparent_background=True)
#             plotter.close()
#             del file_vtu, plotter  # Free memory

#         # --- Crop to specimen bounding box ---
#         img = mpimg.imread(img_path)
#         min_row, max_row, min_col, max_col = get_black_bbox(img)
#         cropped_img = img[min_row:max_row+1, min_col:max_col+1]
#         mpimg.imsave(img_path, cropped_img)
#         del img, cropped_img  # Free memory

#     print(f"Saved images to {output_folder}")


# def skeleton_to_grid(skeleton, dx, dy, x0=0.0, y0=0.0):
#     """
#     Returns x_grid, y_grid, and skeleton_grid (1 for skeleton, 0 elsewhere).
#     skeleton: 2D binary array (output of skeletonize)
#     dx, dy: pixel size in x and y
#     x0, y0: coordinates of the top-left pixel (default 0,0)
#     """
#     ny, nx = skeleton.shape
#     x = x0 + np.arange(nx) * dx
#     y = y0 + np.arange(ny) * dy
#     x_grid, y_grid = np.meshgrid(x, y)
#     skeleton_grid = skeleton.astype(int)
#     return x_grid, y_grid, skeleton_grid


# def obtain_crack_coordinates(skeleton, dx, dy, x0=0.0, y0=0.0):
#     """
#     Returns x_phys, y_phys coordinates of the skeleton points in physical units.
#     skeleton: 2D binary array (output of skeletonize)
#     dx, dy: pixel size in x and y
#     x0, y0: coordinates of the top-left pixel (default 0, 0)
#     """
#     ny, nx = skeleton.shape
#     x = x0 + np.arange(nx) * dx
#     y = y0 + np.arange(ny) * dy
#     x_grid, y_grid = np.meshgrid(x, y)

#     ys, xs = np.where(skeleton == 1)
#     x_phys = x_grid[ys, xs]
#     y_phys = y_grid[ys, xs]

#     # Sort by x_phys from minimum to maximum
#     sort_idx = np.argsort(x_phys)
#     x_phys = x_phys[sort_idx]
#     y_phys = y_phys[sort_idx]
#     return x_phys, y_phys


# def extract_crack_coordinates(input_folder, output_folder, dx, dy):
#     image_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')])
#     os.makedirs(output_folder, exist_ok=True)
#     coord_paths = []
#     for fname in image_files:
#         img_path = os.path.join(input_folder, fname)
#         img = mpimg.imread(img_path)
#         hsv = rgb2hsv(img[..., :3])
#         red_mask = ((hsv[..., 0] < 0.05) | (hsv[..., 0] > 0.95)) & (hsv[..., 1] > 0.5) & (hsv[..., 2] > 0.2)
#         skeleton = skeletonize(red_mask)
#         if np.any(skeleton):
#             x_phys, y_phys = obtain_crack_coordinates(skeleton, dx, dy)
#         else:
#             x_phys, y_phys = [0.0], [0.0]
#         coord_path = os.path.join(output_folder, fname.replace('.png', '.txt'))
#         np.savetxt(coord_path, np.column_stack((x_phys, y_phys)), header="x_phys, y_phys", comments='')
#         coord_paths.append(coord_path)


# def generate_splines_from_coordinates(coord_folder, spline_folder, smoothing=2.0, n_points=1000):
#     """
#     Reads coordinate files, generates splines, and saves spline coordinates to spline_folder.
#     """
#     os.makedirs(spline_folder, exist_ok=True)
#     coord_files = sorted([f for f in os.listdir(coord_folder) if f.endswith('.txt')])
#     for fname in coord_files:
#         coord_path = os.path.join(coord_folder, fname)
#         data = np.loadtxt(coord_path, skiprows=1)
#         if data.size == 0 or (data.ndim == 2 and data.shape[1] < 2):
#             print(f"Skipping empty or malformed file: {coord_path}")
#             continue
#         if data.ndim == 1:
#             data = data[None, :]
#         x_phys, y_phys = data[:, 0], data[:, 1]
#         # Generate spline points
#         if len(x_phys) > 3:
#             tck, u = splprep([x_phys, y_phys], s=smoothing)
#             u_fine = np.linspace(0, 1, n_points)
#             x_spline, y_spline = splev(u_fine, tck)
#             spline_points = np.column_stack((x_spline, y_spline))
#         else:
#             spline_points = np.column_stack((x_phys, y_phys))
#         spline_path = os.path.join(spline_folder, fname.replace('.txt', '_spline.txt'))
#         np.savetxt(spline_path, spline_points, header="x_spline y_spline", comments='')


# def measure_lengths_from_splines(spline_folder):
#     """
#     Reads all spline files in spline_folder and returns an array of their lengths.
#     """
#     spline_files = sorted([f for f in os.listdir(spline_folder) if f.endswith('_spline.txt')])
#     lengths = []
#     for fname in spline_files:
#         spline_path = os.path.join(spline_folder, fname)
#         data = np.loadtxt(spline_path, skiprows=1)
#         if data.size == 0 or (data.ndim == 2 and data.shape[1] < 2):
#             print(f"Skipping empty or malformed spline file: {spline_path}")
#             continue
#         if data.ndim == 1:
#             data = data[None, :]
#         diffs = np.diff(data, axis=0)
#         length = np.sum(np.linalg.norm(diffs, axis=1))
#         lengths.append(length)
#     return np.array(lengths)


# def measure_lengths_from_points(points_folder):
#     """
#     Reads all coordinate files in points_folder and returns an array of their polyline lengths.
#     Each file should contain x, y (and optionally z) columns.
#     """
#     point_files = sorted([f for f in os.listdir(points_folder) if f.endswith('.txt') and not f.endswith('_spline.txt')])
#     lengths = []
#     for fname in point_files:
#         point_path = os.path.join(points_folder, fname)
#         data = np.loadtxt(point_path, skiprows=1)
#         if data.size == 0 or (data.ndim == 2 and data.shape[1] < 2):
#             print(f"Skipping empty or malformed point file: {point_path}")
#             continue
#         if data.ndim == 1:
#             data = data[None, :]
#         diffs = np.diff(data[:, :2], axis=0)  # Only use x and y columns
#         length = np.sum(np.linalg.norm(diffs, axis=1))
#         lengths.append(length)
#     return np.array(lengths)


# def generate_crack_gif_with_length(input_folder, output_folder, crack_lengths, gif_name="crack_evolution.gif"):
#     """
#     Generates a GIF from all PNG images in input_folder, overlaying the crack length on each frame.
#     """
#     image_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')])
#     images = []

#     for idx, (fname, crack_length) in enumerate(zip(image_files, crack_lengths)):
#         img_path = os.path.join(input_folder, fname)
#         img = imageio.imread(img_path)

#         fig, ax = plt.subplots(figsize=(8, 8))
#         ax.imshow(img)
#         ax.axis('off')
#         ax.text(
#             0.05, 0.95,
#             f"Crack length: {crack_length:.3f}",
#             color='yellow', fontsize=18, fontweight='bold',
#             ha='left', va='top', transform=ax.transAxes,
#             bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.5')
#         )
#         ax.set_title(f"Step {idx+1}")
#         fig.canvas.draw()

#         frame = np.asarray(fig.canvas.buffer_rgba())
#         if frame.shape[2] == 4:
#             frame = frame[..., :3]
#         images.append(frame)
#         plt.close(fig)

#     gif_path = os.path.join(output_folder, gif_name)
#     imageio.mimsave(gif_path, images, duration=0.7)
#     print(f"GIF saved to {gif_path}")

# from skimage.transform import resize

# def generate_pyvista_crack_gif(
#     input_folder,
#     output_folder,
#     folder_crack_coordinates,
#     folder_crack_spline,
#     x0=0.0,
#     y0=0.0):
#     """
#     Generates a GIF using PyVista for all time steps, overlaying both experimental and spline lines.
#     """
#     ratio_horizontal_div_vertical=4
#     input_folder = os.path.join(folder_simulation, "paraview-solutions_vtu")
#     output_folder = os.path.join(folder_simulation, "crack_measurement")
#     folder_crack_coordinates = os.path.join(output_folder, "coordinates")
#     folder_crack_spline = os.path.join(output_folder, "spline_coordinates")

#     # Get all time step base names (without extension)
#     base_names = sorted([
#         fname.replace('.txt', '') for fname in os.listdir(folder_crack_coordinates)
#         if fname.endswith('.txt')
#     ])

#     frames = []
#     tmp_img_folder = os.path.join(output_folder, "pyvista_gif_frames")
#     os.makedirs(tmp_img_folder, exist_ok=True)

#     pvtu_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.vtu')])[1:]
    
#     for fname in pvtu_files:
#         file_path = os.path.join(input_folder, fname)
#         file_vtu = pv.read(file_path)

#         # Find corresponding spline file
#         spline_file = os.path.join(folder_crack_spline, fname.replace('.vtu', '_spline.txt'))
#         spline_points = None
#         if os.path.exists(spline_file):
#             data = np.loadtxt(spline_file, skiprows=1)
#             if data.size > 0:
#                 if data.ndim == 1:
#                     data = data[None, :]
#                 # Assume 2D: x, y
#                 x_spline, y_spline = data[:, 0], data[:, 1]
#                 # Build 3D points for PyVista (z=0)
#                 line_points_spline = np.column_stack((x_spline, y_spline, np.zeros_like(x_spline)))
#                 spline_points = line_points_spline

#         plotter = pv.Plotter(off_screen=True)
#         plotter.set_background('white')
#         plotter.add_mesh(file_vtu, scalars='phi', show_scalar_bar=False)
#         if spline_points is not None:
#             line_spline = pv.lines_from_points(spline_points)
#             plotter.add_mesh(line_spline, color='black', line_width=5, label='spline')
#         plotter.camera_position = 'xy'
#         img_path = os.path.join(tmp_img_folder, fname.replace('.vtu', '.png'))
#         plotter.show(auto_close=False, window_size=(int(1024*ratio_horizontal_div_vertical), 1024))
#         plotter.screenshot(img_path, transparent_background=True)
#         plotter.close()
#         frames.append(img_path)

#     # Save GIF
#     gif_path = os.path.join(output_folder, "crack_evolution_pyvista.gif")
#     imageio.mimsave(gif_path, frames, duration=0.7)
#     print(f"GIF saved to {gif_path}")      

#     # Save GIF
#     gif_path = os.path.join(output_folder, "crack_evolution_pyvista.gif")
#     imageio.mimsave(gif_path, frames, duration=0.7)
#     print(f"GIF saved to {gif_path}")

#     # Optionally, clean up temporary images
#     # shutil.rmtree(tmp_img_folder)

# def measure_crack(folder_simulation, physical_horizontal, physical_vertical, threshold=0.95, smoothing=1.0):
#     """
#     Main function to measure crack lengths and generate images and GIF.
#     """
#     input_folder = os.path.join(folder_simulation, "paraview-solutions_vtu")
#     output_folder = os.path.join(folder_simulation, "crack_measurement")

#     folder_phi_threshold_images = os.path.join(output_folder, "phi_threshold_images")
#     folder_phi_images = os.path.join(output_folder, "phi_images")
#     folder_phi_images_splines = os.path.join(output_folder, "phi_images_splines")
#     folder_crack_coordinates = os.path.join(output_folder, "coordinates")
#     folder_crack_spline = os.path.join(output_folder, "spline_coordinates")
   
#     # 1. Generate crack images from .vtu files
#     ratio_horizontal_div_vertical = physical_horizontal / physical_vertical
#     # generate_crack_images(input_folder, folder_phi_images, threshold=None, ratio_horizontal_div_vertical=ratio_horizontal_div_vertical)
#     # generate_crack_images(input_folder, folder_phi_threshold_images, threshold=threshold, ratio_horizontal_div_vertical=ratio_horizontal_div_vertical)

#     # 2. Get the bounding box of the black region in the first image to determine pixel size
#     image_files = sorted([f for f in os.listdir(folder_phi_threshold_images) if f.endswith('.png')])
#     if not image_files:
#         print("No PNG images found in output folder. Exiting.")
#         return

#     img_path = os.path.join(folder_phi_threshold_images, image_files[0])
#     img = mpimg.imread(img_path)
#     if img.size == 0:
#         print("First image is empty. Exiting.")
#         return

#     min_row, max_row, min_col, max_col = get_black_bbox(img)
#     horizontal_pixels = max_col - min_col + 1
#     vertical_pixels = max_row - min_row + 1

#     # Now set your known physical size here:
#     dx = physical_horizontal / horizontal_pixels
#     dy = physical_vertical / vertical_pixels

#     print(f"Detected specimen bounding box: rows {min_row}-{max_row}, cols {min_col}-{max_col}")
#     print(f"Horizontal pixels: {horizontal_pixels}, Vertical pixels: {vertical_pixels}")
#     print(f"Pixel size: dx={dx:.6f}, dy={dy:.6f}")

#     # 3. Extract crack coordinates and save them
#     extract_crack_coordinates(folder_phi_threshold_images, folder_crack_coordinates, dx, dy)

#     generate_splines_from_coordinates(folder_crack_coordinates, folder_crack_spline, smoothing, n_points=1000)
#     # # 4. Measure crack lengths from coordinates
#     lengths = measure_lengths_from_splines(folder_crack_spline)
#     np.savetxt(os.path.join(output_folder, "crack_lengths.txt"), lengths, header="crack_length", comments='')
   
#     lengths_points = measure_lengths_from_points(folder_crack_coordinates)
#     np.savetxt(os.path.join(output_folder, "crack_lengths_points.txt"), lengths_points, header="crack_length", comments='')

#     generate_crack_images(input_folder, folder_phi_images_splines, None, ratio_horizontal_div_vertical, with_spline=True)
    
#     # 5. Generate GIF of crack evolution
#     # generate_crack_gif_with_length(input_folder, output_folder, lengths, gif_name="crack_evolution.gif")
#     # generate_pyvista_crack_gif(input_folder, output_folder, folder_crack_coordinates, folder_crack_spline, x0=0.1, y0=max_col*dy)# from phasefieldx.PostProcessing.measure_crack_length_2d import measure_crack
#     # generate_crack_images(input_folder, folder_phi_images_splines, None, ratio_horizontal_div_vertical, with_spline=True)


# def create_gif_from_images_and_length(folder, output_gif, duration=0.7):
#     """
#     Creates a GIF from a sequence of images in a specified folder, overlaying the crack length from crack_lengths.txt on each frame.

#     Parameters:
#     - folder (str): Path to the folder containing the images and crack_lengths.txt file.
#     - output_gif (str): Path to save the output GIF.
#     - duration (float): Duration for each frame in the GIF (in seconds).
#     """
#     import numpy as np
#     # Get all image files (e.g., PNG, JPG) and sort them
#     images = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

#     # Read crack lengths from crack_lengths.txt in the same folder
#     crack_lengths_path = os.path.join("results_2_a03_l2/crack_measurement", "crack_lengths.txt")
#     if not os.path.exists(crack_lengths_path):
#         raise FileNotFoundError(f"crack_lengths.txt not found in {folder}")
#     lengths = np.loadtxt(crack_lengths_path, skiprows=1)

#     if len(images) != len(lengths):
#         raise ValueError("The number of images and crack lengths in crack_lengths.txt must match.")

#     frames = []
#     for idx, (fname, length) in enumerate(zip(images, lengths)):
#         img = imageio.imread(os.path.join(folder, fname))
#         # Convert to uint8 if needed
#         if img.dtype != 'uint8':
#             img = (img * 255).astype('uint8')
#         # Remove alpha channel if present
#         if img.ndim == 3 and img.shape[-1] == 4:
#             img = img[..., :3]

#         # Overlay the crack length value on the image
#         fig, ax = plt.subplots(figsize=(8, 8))
#         ax.imshow(img)
#         ax.axis('off')
#         ax.text(
#             0.05, 0.95,
#             f"Crack length: {length:.3f}",
#             color='yellow', fontsize=18, fontweight='bold',
#             ha='left', va='top', transform=ax.transAxes,
#             bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.5')
#         )
#         fig.canvas.draw()

#         # Convert the figure to an image
#         frame = np.asarray(fig.canvas.buffer_rgba())
#         if frame.shape[2] == 4:
#             frame = frame[..., :3]
#         frames.append(frame)
#         plt.close(fig)

#     # Save the GIF
#     imageio.mimsave(output_gif, frames, duration=duration)
#     print(f"GIF saved as {output_gif}")


# folder_simulation = "results_simulation_3d"
# input_folder = os.path.join(folder_simulation, "paraview-solutions_vtu")
# output_folder = os.path.join(folder_simulation, "crack_measurement")

# # measure_crack(folder_simulation, physical_horizontal=1.0, physical_vertical=6.0, threshold=0.95, smoothing=0.1)
# create_gif_from_images(folder_simulation+"/crack_measurement/phi_images_splines", output_folder+"/phi_images_splines.gif", duration=5.0)


# # Example usage:
# pvd_file = os.path.join(input_folder, "phasefieldx.pvd")
# output_steps_times = os.path.join(output_folder, "steps_times.txt")
# extract_steps_and_times_from_pvd(pvd_file, output_steps_times)

# # Load step times using numpy (assuming two columns: step and time)
# step_times = np.loadtxt(os.path.join(output_folder, 'steps_times.txt'), skiprows=1, usecols=1).tolist()

# # Load crack lengths using numpy (skip header if present)
# crack_lengths = np.loadtxt(os.path.join(output_folder, 'crack_lengths.txt'), skiprows=1).tolist()
# # crack_lengths.insert(0, 0)

# # Ensure lengths match after adding (0, 0)
# assert len(step_times) == len(crack_lengths), "step_times and crack_lengths must have the same length"

# # Save to new file using numpy
# data = np.column_stack((step_times, crack_lengths))
# np.savetxt(os.path.join(output_folder, 'step_time_crack_length.txt'), data, header="step_time\tcrack_length", fmt="%.8e", comments='')


# step_time_interpolated = np.arange(1, step_times[-1]+1)

# # Create cubic interpolator
# from scipy.interpolate import interp1d
# f = interp1d(step_times, crack_lengths, kind='quadratic', fill_value="extrapolate")

# # Interpolated y values
# crack_lengths_interpolated = f(step_time_interpolated)

# data = np.column_stack((step_time_interpolated, crack_lengths_interpolated))
# np.savetxt(os.path.join(output_folder, 'interpolated_step_time_crack_length.txt'), data, header="step_time\tcrack_length", fmt="%.8e", comments='')

# # measure_crack(folder_simulation, physical_horizontal=1.0, physical_vertical=6.0)