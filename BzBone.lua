-- -*- lua -*-
-- vim:ft=lua:et:ts=4

whatis("Sets up environment for BzBone version 1.0")

local version = "1.02"

-- Initialize module commands
help([[
    Sets up environment for BzBone version ]] .. version)

-- Set environment variables
conflict("python")
conflict("anaconda")
conflict("conda")
conflict("miniconda")
conflict("intelpython")

-- Define paths
local python_path = "/home/u9132064/module/py39_4.12.0"

-- Set environment variables
prepend_path("PATH", pathJoin(python_path, "bin"))
prepend_path("MANPATH", pathJoin(python_path, "share/man"))
prepend_path("LD_LIBRARY_PATH", pathJoin(python_path, "lib"))
prepend_path("LIBRARY_PATH", pathJoin(python_path, "lib"))
prepend_path("CPATH", pathJoin(python_path, "include"))
prepend_path("CMAKE_PREFIX_PATH", python_path)
prepend_path("PYTHONPATH", pathJoin(python_path, "lib/python3.9/site-packages"))

setenv("PYTHON", python_path)
setenv("PYTHONPATH", pathJoin(python_path, "lib/python3.9") .. ":" .. pathJoin(python_path, "lib/python3.9/lib-dynload") .. ":" .. pathJoin(python_path, "lib/python3.9/site-packages"))

-- Provide information
if (mode() == "load") then
    LmodMessage("BzBone version " .. version .. " has been loaded")
end