import numpy as np

cdef extern from "ft2build.h":
    # L'include doit être fait avant le suivant. Atypique?
    pass

cdef extern from "freetype/freetype.h":
    # Note: tous les types entiers coercent en int
    cdef int FT_LOAD_RENDER  # instruction '#define'
    cdef int FT_LOAD_COLOR
    ctypedef int FT_Error

    ctypedef struct FT_LibraryRec_  # on ignore le contenu
    ctypedef FT_LibraryRec_* FT_Library

    ctypedef struct FT_Bitmap:
        int* buffer
        int width
        int rows

    ctypedef struct FT_GlyphSlotRec_:
        FT_Bitmap bitmap
    ctypedef FT_GlyphSlotRec_*  FT_GlyphSlot

    ctypedef struct FT_FaceRec_:
        FT_GlyphSlot glyph
    ctypedef FT_FaceRec_*  FT_Face

    # Les fonctions utilisées dans l'exemple du tutorial

    FT_Error FT_Init_FreeType(FT_Library*)
    FT_Error FT_New_Face(FT_Library, char* filepath, int, FT_Face*)
    FT_Error FT_Done_Face(FT_Face face)

    FT_Error FT_Set_Char_Size(FT_Face, int w, int h, int hres, int vres)
    FT_Error FT_Load_Char(FT_Face, int char_code, int load_flags)

# Initialisation (variable globale)
cdef FT_Library library
FT_Init_FreeType(&library)

cdef class Face:

    cdef FT_Face _face

    def __cinit__(self, str path, int size=48*64, int resolution=72):
        FT_New_Face(library, path.encode('utf-8'), 0, &self._face)
        FT_Set_Char_Size(self._face, size, size, resolution, resolution)

    def load_char(self, str c):
        cdef int i, j
        cdef FT_Bitmap bm
        cdef unsigned char[:, :] char_view

        FT_Load_Char(self._face, ord(c), FT_LOAD_RENDER)
        bm = self._face.glyph.bitmap
        result = np.zeros((bm.rows, bm.width), dtype=np.uint8)
        char_view = result

        for i in range(bm.width):
            for j in range(bm.rows):
                char_view[j, i] = bm.buffer[j*bm.width + i]

        return result