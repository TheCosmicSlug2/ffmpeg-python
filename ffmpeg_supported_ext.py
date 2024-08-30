

def get_ext(file):

    with open(file, "r") as file:
        gigalist = file.readlines()
        for giga_idx in range(len(gigalist)):
            gigalist[giga_idx] = "." + gigalist[giga_idx][5:]

            string = ""
            idx = 0
            while gigalist[giga_idx][idx] != " ":
                string += gigalist[giga_idx][idx]
                idx += 1
            gigalist[giga_idx] = string

        return gigalist

list_ffmpeg_demuxer_supported = ['.3dostr', '.4xm', '.aa', '.aac', '.aax', '.ac3', '.ac4', '.ace', '.acm', '.act',
                                 '.adf', '.adp', '.ads', '.adx', '.aea', '.afc', '.aiff', '.aix', '.alaw', '.alias_pix',
                                 '.alp', '.amr', '.amrnb', '.amrwb', '.anm', '.apac', '.apc', '.ape', '.apm', '.apng',
                                 '.aptx', '.aptx_hd', '.aqtitle', '.argo_asf', '.argo_brp', '.argo_cvg', '.asf',
                                 '.asf_o', '.ass', '.ast', '.au', '.av1', '.avi', '.avr', '.avs', '.avs2', '.avs3',
                                 '.bethsoftvid', '.bfi', '.bfstm', '.bin', '.bink', '.binka', '.bit', '.bitpacked',
                                 '.bmp_pipe', '.bmv', '.boa', '.bonk', '.brender_pix', '.brstm', '.c93', '.caf',
                                 '.cavsvideo', '.cdg', '.cdxl', '.cine', '.codec2', '.codec2raw', '.concat',
                                 '.cri_pipe', '.dash', '.data', '.daud', '.dcstr', '.dds_pipe', '.derf', '.dfa',
                                 '.dfpwm', '.dhav', '.dirac', '.dnxhd', '.dpx_pipe', '.dsf', '.dshow', '.dsicin',
                                 '.dss', '.dts', '.dtshd', '.dv', '.dvbsub', '.dvbtxt', '.dxa', '.ea', '.ea_cdata',
                                 '.eac3', '.epaf', '.evc', '.exr_pipe', '.f32be', '.f32le', '.f64be', '.f64le',
                                 '.ffmetadata', '.film_cpk', '.filmstrip', '.fits', '.flac', '.flic', '.flv', '.frm',
                                 '.fsb', '.fwse', '.g722', '.g723_1', '.g726', '.g726le', '.g729', '.gdigrab', '.gdv',
                                 '.gem_pipe', '.genh', '.gif', '.gif_pipe', '.gsm', '.gxf', '.h261', '.h263', '.h264',
                                 '.hca', '.hcom', '.hdr_pipe', '.hevc', '.hls', '.hnm', '.iamf', '.ico', '.idcin',
                                 '.idf', '.iff', '.ifv', '.ilbc', '.image2', '.image2pipe', '.imf', '.ingenient',
                                 '.ipmovie', '.ipu', '.ircam', '.iss', '.iv8', '.ivf', '.ivr', '.j2k_pipe', '.jacosub',
                                 '.jpeg_pipe', '.jpegls_pipe', '.jpegxl_anim', '.jpegxl_pipe', '.jv', '.kux', '.kvag',
                                 '.laf', '.lavfi', '.libgme', '.libopenmpt', '.live_flv', '.lmlm4', '.loas', '.lrc',
                                 '.luodat', '.lvf', '.lxf', '.m4v', '.matroska,webm', '.mca', '.mcc', '.mgsts',
                                 '.microdvd', '.mjpeg', '.mjpeg_2000', '.mlp', '.mlv', '.mm', '.mmf', '.mods',
                                 '.moflex', '.mov', '.mp4', '.m4a', '.3gp', '.3g2', '.mj2', '.mp3', '.mpc', '.mpc8',
                                 '.mpeg', '.mpegts', '.mpegtsraw', '.mpegvideo', '.mpjpeg', '.mpl2', '.mpsub', '.msf',
                                 '.msnwctcp', '.msp', '.mtaf', '.mtv', '.mulaw', '.musx', '.mv', '.mvi', '.mxf', '.mxg',
                                 '.nc', '.nistsphere', '.nsp', '.nsv', '.nut', '.nuv', '.obu', '.ogg', '.oma',
                                 '.openal', '.osq', '.paf', '.pam_pipe', '.pbm_pipe', '.pcx_pipe', '.pdv', '.pfm_pipe',
                                 '.pgm_pipe', '.pgmyuv_pipe', '.pgx_pipe', '.phm_pipe', '.photocd_pipe', '.pictor_pipe',
                                 '.pjs', '.pmp', '.png_pipe', '.pp_bnk', '.ppm_pipe', '.psd_pipe', '.psxstr', '.pva',
                                 '.pvf', '.qcp', '.qdraw_pipe', '.qoa', '.qoi_pipe', '.r3d', '.rawvideo', '.realtext',
                                 '.redspark', '.rka', '.rl2', '.rm', '.roq', '.rpl', '.rsd', '.rso', '.rtp', '.rtsp',
                                 '.s16be', '.s16le', '.s24be', '.s24le', '.s32be', '.s32le', '.s337m', '.s8', '.sami',
                                 '.sap', '.sbc', '.sbg', '.scc', '.scd', '.sdns', '.sdp', '.sdr2', '.sds', '.sdx',
                                 '.ser', '.sga', '.sgi_pipe', '.shn', '.siff', '.simbiosis_imx', '.sln', '.smjpeg',
                                 '.smk', '.smush', '.sol', '.sox', '.spdif', '.srt', '.stl', '.subviewer',
                                 '.subviewer1', '.sunrast_pipe', '.sup', '.svag', '.svg_pipe', '.svs', '.swf', '.tak',
                                 '.tedcaptions', '.thp', '.tiertexseq', '.tiff_pipe', '.tmv', '.truehd', '.tta', '.tty',
                                 '.txd', '.ty', '.u16be', '.u16le', '.u24be', '.u24le', '.u32be', '.u32le', '.u8',
                                 '.usm', '.v210', '.v210x', '.vag', '.vbn_pipe', '.vc1', '.vc1test', '.vfwcap', '.vidc',
                                 '.vividas', '.vivo', '.vmd', '.vobsub', '.voc', '.vpk', '.vplayer', '.vqf', '.vvc',
                                 '.w64', '.wady', '.wav', '.wavarc', '.wc3movie', '.webm_dash_manifest', '.webp_pipe',
                                 '.webvtt', '.wsaud', '.wsd', '.wsvqa', '.wtv', '.wv', '.wve', '.xa', '.xbin',
                                 '.xbm_pipe', '.xmd', '.xmv', '.xpm_pipe', '.xvag', '.xwd_pipe', '.xwma', '.yop',
                                 '.yuv4mpegpipe', ".txt"] # jrajoute .txt parce que je suis un branleur

list_ffmpeg_muxer_supported = ['.3g2', '.3gp', '.a64', '.ac3', '.ac4', '.adts', '.adx', '.aea', '.aiff', '.alaw',
                               '.alp', '.amr', '.amv', '.apm', '.apng', '.aptx', '.aptx_hd', '.argo_asf', '.argo_cvg',
                               '.asf', '.asf_stream', '.ass', '.ast', '.au', '.avi', '.avif', '.avm2', '.avs2', '.avs3',
                               '.bit', '.caf', '.cavsvideo', '.chromaprint', '.codec2', '.codec2raw', '.crc', '.dash',
                               '.data', '.daud', '.dfpwm', '.dirac', '.dnxhd', '.dts', '.dv', '.dvd', '.eac3', '.evc',
                               '.f32be', '.f32le', '.f4v', '.f64be', '.f64le', '.ffmetadata', '.fifo', '.film_cpk',
                               '.filmstrip', '.fits', '.flac', '.flv', '.framecrc', '.framehash', '.framemd5', '.g722',
                               '.g723_1', '.g726', '.g726le', '.gif', '.gsm', '.gxf', '.h261', '.h263', '.h264',
                               '.hash', '.hds', '.hevc', '.hls', '.iamf', '.ico', '.ilbc', '.image2', '.image2pipe',
                               '.ipod', '.ircam', '.ismv', '.ivf', '.jacosub', '.kvag', '.latm', '.lrc', '.m4v',
                               '.matroska', '.md5', '.microdvd', '.mjpeg', '.mkvtimestamp_v2', '.mlp', '.mmf', '.mov',
                               '.mp2', '.mp3', '.mp4', '.mpeg', '.mpeg1video', '.mpeg2video', '.mpegts', '.mpjpeg',
                               '.mulaw', '.mxf', '.mxf_d10', '.mxf_opatom', '.null', '.nut', '.obu', '.oga', '.ogg',
                               '.ogv', '.oma', '.opus', '.psp', '.rawvideo', '.rcwt', '.rm', '.roq', '.rso', '.rtp',
                               '.rtp_mpegts', '.rtsp', '.s16be', '.s16le', '.s24be', '.s24le', '.s32be', '.s32le',
                               '.s8', '.sap', '.sbc', '.scc', '.sdl,sdl2', '.segment', '.smjpeg', '.smoothstreaming',
                               '.sox', '.spdif', '.spx', '.srt', '.stream_segment,ssegment', '.streamhash', '.sup',
                               '.svcd', '.swf', '.tee', '.truehd', '.tta', '.ttml', '.u16be', '.u16le', '.u24be',
                               '.u24le', '.u32be', '.u32le', '.u8', '.uncodedframecrc', '.vc1', '.vc1test', '.vcd',
                               '.vidc', '.vob', '.voc', '.vvc', '.w64', '.wav', '.webm', '.webm_chunk',
                               '.webm_dash_manifest', '.webp', '.webvtt', '.wsaud', '.wtv', '.wv', '.yuv4mpegpipe']





























