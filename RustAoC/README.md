## Rust Learning Project

# Basics

1) Create a self contained project

cargo new project_name --vcs none

The --vcs none flag prevents it from creating additional git repos.

Additionally we can modify ~/.cargo/config to have this in it to stop the vcs creation.

[package]
vcs = "none"


