-- Use folder name to build extension name and tag.
local ext = get_current_extension_info()

project_ext (ext)

-- Link only those files and folders into the extension target directory
repo_build.prebuild_link {
    { "data", ext.target_dir.."/data" },
    { "layouts", ext.target_dir.."/layouts" },
    { "physical_ai_learning", ext.target_dir.."/physical_ai_learning" },
}
