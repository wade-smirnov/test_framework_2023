class Mediatype:
    xods = "application/vnd.collabio.xodocuments.spreadsheet"
    xodt = "application/vnd.collabio.xodocuments.document"
    odt = "application/vnd.oasis.opendocument.text"
    ods = "application/vnd.oasis.opendocument.spreadsheet"
    odp = "application/vnd.oasis.opendocument.presentation"
    co_document_template = "application/vnd.collabio.xodocuments.document-template"
    co_spreadsheet = "application/vnd.collabio.xodocuments.spreadsheet"
    co_spreadsheet_template = (
        "application/vnd.collabio.xodocuments.spreadsheet-template"
    )
    co_presentation = "application/vnd.collabio.xodocuments.presentation"
    co_presentation_template = (
        "application/vnd.collabio.xodocuments.presentation-template"
    )
    co_folder = "application/vnd.ncloudtech.cloudoffice.folder"
    co_index = "application/vnd.ncloudtech.cloudoffice.plain-idx"
    serialized_dom = "application/vnd.ncloudtech.cloudoffice.internal.dom"
    serialized_prerender = "application/vnd.ncloudtech.cloudoffice.internal.pregen"

    # ms - mediatypes
    oxml_document = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    oxml_document_template = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.template"
    )
    oxml_spreadsheet = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    oxml_spreadsheet_template = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.template"
    )
    oxml_presentation = (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    oxml_presentation_template = (
        "application/vnd.openxmlformats-officedocument.presentationml.template"
    )
    oxml_presentation_show = (
        "application/vnd.openxmlformats-officedocument.presentationml.slideshow"
    )
    ms_bin_document = "application/msword"
    ms_bin_document_macro = "application/vnd.ms-word.document.macroenabled.12"
    ms_bin_document_template_macro = "application/vnd.ms-word.template.macroenabled.12"
    ms_bin_spreadsheet = "application/vnd.ms-excel"
    ms_bin_spreadsheet_macro = "application/vnd.ms-excel.sheet.macroenabled.12"
    ms_bin_spreadsheet_template_macro = (
        "application/vnd.ms-excel.template.macroenabled.12"
    )
    ms_bin_presentation = "application/vnd.ms-powerpoint"
    ms_bin_presentation_macro = (
        "application/vnd.ms-powerpoint.presentation.macroenabled.12"
    )
    ms_bin_presentation_template_macro = (
        "application/vnd.ms-powerpoint.template.macroenabled.12"
    )
    ms_bin_presentation_show_macro = (
        "application/vnd.ms-powerpoint.slideshow.macroenabled.12"
    )
    ms_portable_executable = "application/vnd.microsoft.portable-executable"

    # open office - mediatypes
    odf_text = "application/vnd.oasis.opendocument.text"
    odf_text_template = "application/vnd.oasis.opendocument.text-template"
    odf_spreadsheet = "application/vnd.oasis.opendocument.spreadsheet"
    odf_spreadsheet_template = "application/vnd.oasis.opendocument.spreadsheet-template"
    odf_presentation = "application/vnd.oasis.opendocument.presentation"
    odf_presentation_template = (
        "application/vnd.oasis.opendocument.presentation-template"
    )

    # images mediatypes
    svg = "image/svg+xml"
    jpeg = "image/jpeg"
    png = "image/png"
    gif = "image/gif"
    bmp = "image/bmp"
    x_ms_bmp = "image/x-ms-bmp"
    tiff = "image/tiff"
    emf = "application/emf"
    wmf = "application/wmf"
    ico = "application/x-icon"
    wbmp = "image/vnd.wap.wbmp"

    # archives
    gzip = "application/gzip"
    zip = "application/zip"
    sevenz = "application/x-7z-compressed"
    tar = "application/x-tar"
    jar = "application/java-archive"
    rar = "application/x-rar-compressed"
    bz2 = "application/x-bzip2"

    # audio mediatypes
    audio_mpeg = "audio/mpeg"
    wave = "audio/vnd.wave"
    flac = "audio/flac"
    aiff = "audio/x-aiff"
    oga = "audio/vorbis"
    mid = "audio/midi"
    snd = "audio/basic"
    ogg = "audio/ogg"
    wav = "audio/x-wav"
    wma = "audio/x-ms-wma"

    # video mediatypes
    avi = "video/x-msvideo"
    flv = "video/x-flv"
    mkv = "video/x-matroska"
    m4v = "video/x-m4v"
    threegp = "video/3gpp"
    mp4 = "video/mp4"
    mpeg = "video/mpeg"
    qt = "video/quicktime"
    wmv = "video/x-ms-wmv"

    # Microsoft Office MIME types
    doc = "application/msword"
    dot = "application/msword"
    docx = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    dotx = "application/vnd.openxmlformats-officedocument.wordprocessingml.template"
    docm = "application/vnd.ms-word.document.macroEnabled.12"
    dotm = "application/vnd.ms-word.template.macroEnabled.12"
    xls = "application/vnd.ms-excel"
    xlt = "application/vnd.ms-excel"
    xla = "application/vnd.ms-excel"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    xltx = "application/vnd.openxmlformats-officedocument.spreadsheetml.template"
    xlsm = "application/vnd.ms-excel.sheet.macroEnabled.12"
    xltm = "application/vnd.ms-excel.template.macroEnabled.12"
    xlam = "application/vnd.ms-excel.addin.macroEnabled.12"
    xlsb = "application/vnd.ms-excel.sheet.binary.macroEnabled.12"
    ppt = "application/vnd.ms-powerpoint"
    pot = "application/vnd.ms-powerpoint"
    pps = "application/vnd.ms-powerpoint"
    ppa = "application/vnd.ms-powerpoint"
    pptx = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    potx = "application/vnd.openxmlformats-officedocument.presentationml.template"
    ppsx = "application/vnd.openxmlformats-officedocument.presentationml.slideshow"
    ppam = "application/vnd.ms-powerpoint.addin.macroEnabled.12"
    pptm = "application/vnd.ms-powerpoint.presentation.macroEnabled.12"
    potm = "application/vnd.ms-powerpoint.template.macroEnabled.12"
    ppsm = "application/vnd.ms-powerpoint.slideshow.macroEnabled.12"
    mdb = "application/vnd.ms-access"

    # other mediatypes
    pdf = "application/pdf"
    html = "text/html"
    txt = "text/plain"
    csv = "text/csv"
    rtf = "application/rtf"
    json = "application/json"
    json_gz = "application/json+gz"
    url_form = "application/x-www-form-urlencoded"
    tab_separated = "text/tab-separated-values"
    bat = "application/x-msdos-program"
    xml = "application/xml"
    ipa = "application/x-itunes-ip"
    apk = "application/vnd.android.package-archive"
    msi = "application/x-ms-installer"

    # signature
    sig = "application/vnd.ncloudtech.cloudoffice.signature"
