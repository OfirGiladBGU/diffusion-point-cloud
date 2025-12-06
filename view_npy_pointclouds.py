"""
Script to visualize .npy files as point clouds in Open3D viewer.
Recursively searches for .npy files in results directory and allows viewing them.
"""

import os
import argparse
import numpy as np
import open3d as o3d


def find_npy_files(root_dir='./results'):
    """Recursively find all .npy files in the results directory."""
    npy_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.npy'):
                npy_files.append(os.path.join(root, file))
    return sorted(npy_files)


def load_point_cloud(file_path):
    """Load a .npy file and convert to Open3D PointCloud."""
    data = np.load(file_path)
    
    # Handle different data shapes
    if len(data.shape) == 2:
        # Single point cloud
        points = data
    elif len(data.shape) == 3:
        # Multiple point clouds - use first one
        print(f"  Shape: {data.shape} (using first point cloud)")
        points = data[0]
    else:
        raise ValueError(f"Unexpected data shape: {data.shape}")
    
    # Ensure float32
    points = points.astype(np.float32)
    
    # Create Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    return pcd


def view_single_file(file_path):
    """View a single .npy file."""
    print(f"\nLoading: {file_path}")
    try:
        pcd = load_point_cloud(file_path)
        print(f"  Points: {len(pcd.points)}")
        
        # Visualize
        o3d.visualization.draw_geometries([pcd])
    except Exception as e:
        print(f"  Error: {e}")


def view_multiple_files(file_paths, side_by_side=False):
    """View multiple .npy files."""
    pcds = []
    colors = [
        [1, 0, 0],      # Red
        [0, 1, 0],      # Green
        [0, 0, 1],      # Blue
        [1, 1, 0],      # Yellow
        [1, 0, 1],      # Magenta
        [0, 1, 1],      # Cyan
    ]
    
    for idx, file_path in enumerate(file_paths):
        print(f"\nLoading: {file_path}")
        try:
            pcd = load_point_cloud(file_path)
            print(f"  Points: {len(pcd.points)}")
            
            # Color points if viewing multiple side-by-side
            if side_by_side and len(file_paths) > 1:
                color = colors[idx % len(colors)]
                pcd.paint_uniform_color(color)
            
            pcds.append(pcd)
        except Exception as e:
            print(f"  Error: {e}")
    
    if pcds:
        o3d.visualization.draw_geometries(pcds)


def interactive_viewer(npy_files):
    """Interactive menu to select and view point clouds."""
    if not npy_files:
        print("No .npy files found!")
        return
    
    print("\n" + "="*60)
    print("POINT CLOUD VIEWER")
    print("="*60)
    print(f"\nFound {len(npy_files)} .npy file(s):\n")
    
    for idx, file in enumerate(npy_files, 1):
        print(f"  {idx}. {file}")
    
    while True:
        print("\nOptions:")
        print("  (1-N) View specific file")
        print("  (a)   View all files together")
        print("  (q)   Quit")
        
        choice = input("\nEnter choice: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'a':
            view_multiple_files(npy_files, side_by_side=True)
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(npy_files):
                    view_single_file(npy_files[idx])
                else:
                    print("Invalid selection!")
            except ValueError:
                print("Invalid input!")


def main():
    parser = argparse.ArgumentParser(
        description='Visualize .npy point cloud files using Open3D'
    )
    parser.add_argument(
        '--file',
        type=str,
        default=None,
        help='Specific .npy file to view'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='./results',
        help='Directory to search for .npy files (default: ./results)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='View all found .npy files together'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        default=True,
        help='Launch interactive menu (default)'
    )
    
    args = parser.parse_args()
    
    # View specific file if provided
    if args.file:
        if os.path.exists(args.file):
            view_single_file(args.file)
        else:
            print(f"File not found: {args.file}")
        return
    
    # Find all .npy files
    npy_files = find_npy_files(args.dir)
    
    if not npy_files:
        print(f"No .npy files found in {args.dir}")
        return
    
    # View all files together if requested
    if args.all:
        view_multiple_files(npy_files, side_by_side=True)
        return
    
    # Launch interactive viewer
    if args.interactive:
        interactive_viewer(npy_files)
    else:
        print(f"Found {len(npy_files)} .npy file(s)")
        for file in npy_files:
            print(f"  - {file}")


if __name__ == '__main__':
    main()
