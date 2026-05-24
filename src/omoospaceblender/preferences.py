import bpy
from pathlib import Path

CATEGORY_FOLDER_DEFAULTS = {
    "images": "images",
    "volumes": "volumes",
    "dynamics": "dynamics",
    "libraries": "libraries",
    "misc": "misc",
    "renders": "renders",
    "videos": "videos",
    "audios": "audios",
    "geonodes": "geonodes",
}


class OmoospacePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    omoospace_home: bpy.props.StringProperty(
        name="Home Directory",
        subtype="DIR_PATH",
        default=str(Path.home())
    )  # type: ignore

    category_images: bpy.props.StringProperty(
        name="Images Folder",
        default=CATEGORY_FOLDER_DEFAULTS["images"],
    )  # type: ignore

    category_volumes: bpy.props.StringProperty(
        name="Volumes Folder",
        default=CATEGORY_FOLDER_DEFAULTS["volumes"],
    )  # type: ignore

    category_dynamics: bpy.props.StringProperty(
        name="Dynamics Folder",
        default=CATEGORY_FOLDER_DEFAULTS["dynamics"],
    )  # type: ignore

    category_libraries: bpy.props.StringProperty(
        name="Libraries Folder",
        default=CATEGORY_FOLDER_DEFAULTS["libraries"],
    )  # type: ignore

    category_misc: bpy.props.StringProperty(
        name="Misc Folder",
        default=CATEGORY_FOLDER_DEFAULTS["misc"],
    )  # type: ignore

    category_renders: bpy.props.StringProperty(
        name="Renders Folder",
        default=CATEGORY_FOLDER_DEFAULTS["renders"],
    )  # type: ignore

    category_videos: bpy.props.StringProperty(
        name="Videos Folder",
        default=CATEGORY_FOLDER_DEFAULTS["videos"],
    )  # type: ignore

    category_audios: bpy.props.StringProperty(
        name="Audios Folder",
        default=CATEGORY_FOLDER_DEFAULTS["audios"],
    )  # type: ignore

    category_geonodes: bpy.props.StringProperty(
        name="Geo-nodes Folder",
        default=CATEGORY_FOLDER_DEFAULTS["geonodes"],
    )  # type: ignore

    def draw(self, context):
        layout = self.layout

        layout.label(text="Configuration")
        layout.prop(self, 'omoospace_home')

        layout.separator()
        layout.label(text="Category Folder Names")

        col = layout.column()
        col.prop(self, 'category_images')
        col.prop(self, 'category_videos')
        col.prop(self, 'category_volumes')
        col.prop(self, 'category_dynamics')
        col.prop(self, 'category_libraries')
        col.prop(self, 'category_misc')
        col.prop(self, 'category_renders')
        col.prop(self, 'category_audios')
        col.prop(self, 'category_geonodes')
