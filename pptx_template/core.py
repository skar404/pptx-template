# core.py - public API
# coding=utf-8

import re
import logging
import copy

import six
import pptx_template.pptx_util as util
import pptx_template.text as txt
import pptx_template.chart as ch

log = logging.getLogger()


def _get_id(text, index):
    reg = re.search(r"{id:(?P<id_slide>\w+)}", text)
    if reg:
        slide_id = reg.group('id_slide')
        new_id = '{}_{}'.format(slide_id, index)
        return '{{id:{}}}'.format(new_id), new_id
    return False, None


def _get_blank_slide_layout(pres):
    layout_items_count = [len(layout.placeholders)
                          for layout in pres.slide_layouts]
    min_items = min(layout_items_count)
    blank_layout_id = layout_items_count.index(min_items)
    return pres.slide_layouts[blank_layout_id]


def move_slide(pres, old_index, new_index):
    xml_slides = pres.slides._sldIdLst  # pylint: disable=W0212
    slides = list(xml_slides)
    xml_slides.remove(slides[old_index])
    xml_slides.insert(new_index, slides[old_index])


def _duplicate_slide(pres, index, count):
    """
    Duplicate the slide with the given index in pres.
    Adds slide to the end of the presentation

    Не знаю как это разотает, но это создает копию слайда
    """

    source = pres.slides[index]
    blank_slide_layout = _get_blank_slide_layout(pres)

    dest = pres.slides.add_slide(blank_slide_layout)

    for shape in source.shapes:
        newel = copy.deepcopy(shape.element)
        dest.shapes._spTree.insert_element_before(newel, 'p:extLst')

    for key, value in six.iteritems(source.part.rels):
        # Make sure we don't copy a notesSlide relation as that won't exist
        if "notesSlide" not in value.reltype:
            dest.part.rels.add_relationship(value.reltype,
                                            value._target,
                                            value.rId)

    move_slide(pres, len(list(pres.slides)) - 1, index + 1)

    # Проходим по всем тектовым элементам и переименовываем элементы
    slide_id = None
    for shape in txt.select_all_text_shapes(pres.slides[index + 1]):
        _new_id, name = _get_id(shape.text, count)
        if _new_id:
            slide_id = name
            shape.text = _new_id
            break
    return slide_id


def duplicate_slides(pres, index, count):
    slide_id_list = []
    for i in reversed(range(count)):
        slide_id_list.append(_duplicate_slide(pres, index, i))
    return slide_id_list


def edit_slide(slide, model, skip_model_not_found=False, clear_tags=False):
    """
        1つのスライドに対して文字列置換およびチャートCSV設定を行う
        チャート設定や文字列置換は1スライドに対して複数持てる。配列やdictなどで引渡し、pptxからはEL式で特定する
        チャート設定なのか文字列置換なのかは、EL式の配置されているpptx内のオブジェクトで判断される
        文字列置換やチャートタイトルに EL式で {answer.0} のような形で指定する
        チャート設定として指定可能な項目:
         - file_name : CSVファイルの名前
         - body: CSVファイルの中身そのものを直接文字列で指定できる(file_name, file_encodingは無視される)
         - value_axis_max: チャート左側軸の最大値。(省略可)
         - value_axix_min: チャート左側軸の最小値。(省略可)
         - (TBI) file_encoding: CSVファイルのエンコーディング。省略時は utf-8
    """

    # pptx内の TextFrame の EL表記を model の値で置換する
    for shape in txt.select_all_text_shapes(slide):
        try:
            txt.replace_all_els_in_text_frame(shape.text_frame, model, clear_tags)
        except:
            if not skip_model_not_found:
                raise

    for shape in txt.select_all_tables(slide):
        try:
            txt.replace_all_els_in_table(shape, model, skip_model_not_found, clear_tags)
        except:
            if not skip_model_not_found:
                raise

    # pptx内の 各チャートに対してcsvの値を設定する
    for chart in ch.select_all_chart_shapes(slide):
        try:
            ch.load_data_into_chart(chart, model)
        except:
            if not skip_model_not_found:
                raise


def remove_slide(presentation, slide):
    """
     presentation から 指定した slide を削除する
    """
    util.remove_slide(presentation, slide)


def remove_slide_id(presentation, slide_id):
    """
         指定した id のスライドから {id:foobar} という形式の文字列を削除する
    """
    slide = get_slide(presentation, slide_id)
    for shape in txt.select_all_text_shapes(slide):
        if txt.extract_slide_id(shape.text) == slide_id:
            shape.text = ''


def remove_all_slides_having_id(presentation):
    """
         {id:foobar} という文字列を持つすべてのスライドを削除する
    """
    unused_slides = []
    for slide in presentation.slides:
        for shape in txt.select_all_text_shapes(slide):
            slide_id = txt.extract_slide_id(shape.text)
            if slide_id:
                unused_slides.append((slide_id, slide))
                break
    for slide_id, slide in unused_slides:
        log.info("Removing unused slide_id: %s" % slide_id)
        remove_slide(presentation, slide)


def get_slide(presentation, slide_id):
    """
         指定した id に対して {id:foobar} という TextFrame を持つスライドを探す
    """
    for slide in presentation.slides:
        for shape in txt.select_all_text_shapes(slide):
            if txt.extract_slide_id(shape.text) == slide_id:
                return slide
    raise ValueError(u"slide id:%s not found" % slide_id)
