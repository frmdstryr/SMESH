import os
import shutil
import sys

import patch
from glob import glob


def prepare_netgen():
    """
    Prepare sources for Netgen.
    """
    # Delete source directories if they exist
    if os.path.exists('src/Netgen'):
        shutil.rmtree('src/Netgen')

    # Copy sources
    shutil.copytree('external/Netgen/libsrc', 'src/Netgen/libsrc')
    shutil.copytree('external/Netgen/nglib', 'src/Netgen/nglib')
    shutil.copytree('external/Netgen/rules', 'src/Netgen/rules')

    # Patch Netgen sources for SALOME
    #pset = patch.fromfile('external/NETGENPlugin/src/NETGEN/netgen62ForSalome.patch')
    #success = pset.apply(strip=1, root='src/Netgen')
    #if not success:
    #    raise RuntimeError(f'Failed to apply netgen62ForSalome.patch.')

    #if sys.platform == 'win32':
    #    pset = patch.fromfile('external/NETGENPlugin/src/NETGEN/netgen53ForWindows.patch')
    #    pset.apply(strip=1, root='src/Netgen')

    for patch_file in glob('patch/Netgen_*.patch'):
        pset = patch.fromfile(patch_file)
        assert pset, f"Patch {patch_file} is malformed or not a patch"
        success = pset.apply(strip=0, root='src/Netgen')
        if not success:
            raise RuntimeError(f'Failed to apply {patch_file}.')

    # Copy Netgen cmake files into source directory
    shutil.copytree('cmake/Netgen', 'src/Netgen', dirs_exist_ok=True)


def prepare_kernel():
    """
    Prepare sources for Kernel.
    """
    # Delete source directories if they exist
    if os.path.exists('src/Kernel'):
        shutil.rmtree('src/Kernel')

    # Copy sources
    shutil.copytree('external/Kernel/src/Basics',
                    'src/Kernel/src/Basics')
    shutil.copytree('external/Kernel/src/SALOMELocalTrace',
                    'src/Kernel/src/SALOMELocalTrace')
    shutil.copytree('external/Kernel/src/Utils',
                    'src/Kernel/src/Utils')

    # Copy and overwrite the Kernel CMakeLists.txt file
    target = os.path.join('src/Kernel', 'CMakeLists.txt')
    shutil.copyfile('cmake/Kernel/CMakeLists.txt', target)

    # Patch sources
    pset = patch.fromfile('patch/Kernel.patch')
    success = pset.apply(strip=0, root='src/Kernel')
    if not success:
        raise RuntimeError('Failed to apply Kernel patch.')


def prepare_geom():
    """
    Prepare sources for Geom.
    """
    # Delete source directories if they exist
    if os.path.exists('src/Geom'):
        shutil.rmtree('src/Geom')

    # Copy sources
    shutil.copytree('external/Geom/src/GEOMUtils',
                    'src/Geom/src/GEOMUtils')

    # Patch sources
    pset = patch.fromfile('patch/geom.patch')
    success = pset.apply(strip=0, root='src/Geom')
    if not success:
        raise RuntimeError('Failed to apply SMESH patch.')

    # Copy and overwrite the Geom CMakeLists.txt file
    target = os.path.join('src/Geom', 'CMakeLists.txt')
    shutil.copyfile('cmake/Geom/CMakeLists.txt', target)


def prepare_smesh():
    """
    Prepare sources for SMESH.
    """
    # Delete source directories if they exist
    if os.path.exists('src/SMESH'):
        shutil.rmtree('src/SMESH')

    # Copy sources
    shutil.copytree('external/SMESH/src',
                    'src/SMESH/src')

    # Copy and overwrite the SMESH CMakeLists.txt file
    target = os.path.join('src/SMESH', 'CMakeLists.txt')
    shutil.copyfile('cmake/SMESH/CMakeLists.txt', target)

    # Patch sources
    #pset = patch.fromfile('patch/SMESH.patch')
    #success = pset.apply(strip=0, root='src/SMESH')
    #if not success:
    #    raise RuntimeError('Failed to apply SMESH patch.')

    # Patch sources
    pset = patch.fromfile('patch/mefisto.patch')
    success = pset.apply(strip=0, root='src/SMESH')
    if not success:
        raise RuntimeError('Failed to apply mefisto patch.')

    # Patch source
    for patch_file in glob('patch/SMESH_*.patch'):
        pset = patch.fromfile(patch_file)
        assert pset, f"Patch {patch_file} is malformed or not a patch"
        success = pset.apply(strip=0, root='src/SMESH')
        if not success:
            raise RuntimeError(f'Failed to apply {patch_file}.')

    # Copy MeshVSLink sources
    shutil.copytree('extra/MeshVSLink',
                    'src/SMESH/src/MeshVSLink', dirs_exist_ok=True)

    # Copy MEFISTO2 trte.c source
    shutil.copyfile('extra/MEFISTO2/trte.c', 'src/SMESH/src/MEFISTO2/trte.c')


def prepare_netgen_plugin():
    """
    Prepare sources for NETGENPlugin
    """
    # Delete source directories if they exist
    if os.path.exists('src/SMESH/src/NETGENPlugin'):
        shutil.rmtree('src/SMESH/src/NETGENPlugin')

    # Copy sources
    shutil.copytree('external/NETGENPlugin/src',
                    'src/SMESH/src/NETGENPlugin/src')

    # Patch sources
    for patch_file in glob('patch/NETGENPlugin_*.patch'):
        pset = patch.fromfile(patch_file)
        assert pset, f"Patch {patch_file} is malformed or not a patch"
        success = pset.apply(strip=0, root='src/SMESH/src/NETGENPlugin')
        if not success:
            raise RuntimeError(f"Failed to apply {patch_file}.")


def prepare_noexcept():
    """
    change throw to noexcept to align with c++17
    """
    os.system("grep -rl 'throw(SALOME_Exception)' ./src | xargs sed -i 's/throw(SALOME_Exception)/noexcept(false)/g'")
    os.system("grep -rl 'throw( SALOME_Exception )' ./src | xargs sed -i 's/throw( SALOME_Exception )/noexcept(false)/g'")
    os.system("grep -rl 'throw (SALOME_Exception)' ./src | xargs sed -i 's/throw (SALOME_Exception)/noexcept(false)/g'")
    os.system("grep -rl 'throw ( SALOME_Exception )' ./src | xargs sed -i 's/throw ( SALOME_Exception )/noexcept(false)/g'")
    os.system("grep -rl 'throw (std::bad_alloc)' ./src | xargs sed -i 's/throw (std::bad_alloc)/noexcept(false)/g'")


if __name__ == '__main__':
    prepare_netgen()
    prepare_kernel()
    prepare_geom()
    prepare_smesh()
    prepare_netgen_plugin()
    # prepare_noexcept()


