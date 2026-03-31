#include "game/scns/menu/PageAbout.h"

#include "engine/data/RLE.h"
#include "engine/helper/StrUtil.h"
#include "engine/io/IOUtil.h"
#include "game/FileUtil.h"
#include "game/Global.h"
#include "game/ScreenUtil.h"
#include "game/scns/menu/PageMain.h"
#include "game/scns/menu/PageMsgOK.h"
#include "game/scns/menu/PageMsgYN.h"
#include "game/scns/menu/Scene.h"

#include "game/scns/edit/Scene.h"

using namespace game::scns::menu;
namespace ass = game::assets;

#pragma region macros

#define NOCHAR { .value = 0, .escape = false, }

#pragma endregion

#pragma region init

PageAbout::PageAbout(Scene& scene) : Page(scene)
{
    // Screens
    f_ScreenT = nullptr;
    f_ScreenB = nullptr;
    // Texts
    f_Texts_Title = nullptr;
    f_Texts_Content = nullptr;
    // Content buffer
    f_Content = nullptr;
}

PageAbout::~PageAbout()
{
    // Content buffer
    DELETE_ARRAY(f_Content);
    // Texts
    DELETE_ARRAY(f_Texts_Title)
    DELETE_ARRAY(f_Texts_Content)
    // Screens
    DELETE_ARRAY(f_ScreenB)
    DELETE_ARRAY(f_ScreenT)
}

#pragma endregion

#pragma region helper functions

void PageAbout::m_enter()
{
    game::scns::menu::Page::m_enter();
    // Initialize screen data
    ScreenUtil::load(ass::MenuAboutT::data, ass::MenuAboutT::size, f_ScreenT, f_ScreenT_Len);
    std::copy(f_ScreenT, f_ScreenT + f_ScreenT_Len, scene().titleGFX().bg_Buffer());
    ScreenUtil::load(ass::MenuAboutB::data, ass::MenuAboutB::size, f_ScreenB, f_ScreenB_Len);
    std::copy(f_ScreenB, f_ScreenB + f_ScreenB_Len, scene().textGFX().bg_Buffer());
    // Initialize texts
    m_GetTexts(f_Texts_Count, f_Texts_Title, f_Texts_Content);
    // Initialize input
    f_But_Index = 0x00;
    f_But_Touch = 0xFF;
    f_Tch_Index = 0xFF;
    f_Tch_Touch = 0xFF;
    f_Touching = false;
    // Initialize content
    f_TextIndex = 0;
    if (f_TextIndex < f_Texts_Count)
    {
        f_Title = f_Texts_Title[f_TextIndex];
        m_SetContent(f_Texts_Content[f_TextIndex]);
    }
    // Post-init
    m_Refresh();
}

void PageAbout::m_exit()
{
    // Call base
    Page::m_exit();
}

void PageAbout::m_update()
{
    Page::m_update();
    // Get touch
    if (scene().input_Touch())
    {
        u16 touch_X = (scene().input_Touch_Pos().px) / 8;
        u16 touch_Y = (scene().input_Touch_Pos().py) / 8;
        f_But_Touch = m_GetTouched(touch_X, touch_Y, 
            ass::MenuAboutB::buttons_x, ass::MenuAboutB::buttons_y,
            ass::MenuAboutB::buttons_w, ass::MenuAboutB::buttons_h,
            ass::MenuAboutB::buttons_count);
        f_Tch_Touch = (f_But_Touch < ass::MenuAboutB::buttons_count) ? 0xFF :
            m_GetTouched(touch_X, touch_Y, 
                ass::MenuAboutB::tchbtns_x, ass::MenuAboutB::tchbtns_y,
                ass::MenuAboutB::tchbtns_w, ass::MenuAboutB::tchbtns_h,
                ass::MenuAboutB::tchbtns_count);
    }
    // Get input
    if (scene().input_Down() & KEY_A)
    {
        m_ButtonAction();
    }
    else if (scene().input_Down() & KEY_B)
    {
        m_Close();
    }
    else if (scene().input_Down() & KEY_LEFT)
    {
        if (f_But_Index > 0)
        {
            --f_But_Index;
            f_Touching = false;
            f_Tch_Index = 0xFF;
        }
        m_Refresh_Buttons();
    }
    else if (scene().input_Down() & KEY_RIGHT)
    {
        if ((f_But_Index + 1) < ass::MenuAboutB::buttons_count)
        {
            ++f_But_Index;
            f_Touching = false;
            f_Tch_Index = 0xFF;
        }
        m_Refresh_Buttons();
    }
    else if (scene().input_Repeat() & KEY_UP)
    {
        m_View_Dec(1);
    }
    else if (scene().input_Repeat() & KEY_DOWN)
    {
        m_View_Inc(1);
    }
    else if (scene().input_Down() & KEY_TOUCH)
    {
        if (f_But_Touch < ass::MenuAboutB::buttons_count)
        {
            f_But_Index = f_But_Touch;
            f_Touching = true;
        }
        else if (f_Tch_Touch < ass::MenuAboutB::tchbtns_count)
        {
            f_Tch_Index = f_Tch_Touch;
            m_PageNav();
            f_Touching = true;
        }
        m_Refresh_Buttons();
    }
    else if (scene().input_Repeat() & KEY_TOUCH)
    {
        if (f_Tch_Touch == f_Tch_Index) m_PageNav();
    }
    else if (scene().input_Up() & KEY_TOUCH)
    {
        if (f_But_Touch < ass::MenuAboutB::buttons_count && f_But_Touch == f_But_Index)
            m_ButtonAction();
        f_Touching = false;
        f_Tch_Index = 0xFF;
        m_Refresh_Buttons();
    }
}

void PageAbout::m_vblank()
{
    Page::m_vblank();
}

void PageAbout::m_Add_Word(
    std::vector<std::string>& lines, std::ostringstream& os, size_t& lineLen, 
    std::string::const_iterator beg, std::string::const_iterator end, char endChar)
{
    u16 len = end - beg;
    end = beg + len; // Fix end in case an overflow occurs
    // Newline needed?
    if (lineLen > 0 && (lineLen + len) > DS_SCREEN_COLS)
    {
        lines.push_back(os.str());
        os.str(""); os.clear(); lineLen = 0;
    }
    // Draw text
    if (len <= DS_SCREEN_COLS)
    {
        while (beg != end) { os << *beg; ++beg; ++lineLen; }
    }
    else
    {
        while (beg != end)
        {
            // Newline?
            if (lineLen >= DS_SCREEN_COLS)
            {
                lines.push_back(os.str());
                os.str(""); os.clear(); lineLen = 0;
            }
            // Draw character
            if ((lineLen + 1) == DS_SCREEN_COLS && (beg + 1) != end)
                os << '-';
            else
                os << *(beg++);
            // Next
            ++lineLen;
        }
    }
    // Draw end character
    if (lineLen < DS_SCREEN_COLS)
    {
        if (endChar == '\n')
        {
            lines.push_back(os.str());
            os.str(""); os.clear(); lineLen = 0;
        }
        else if (endChar >= ' ') {  os << endChar; ++lineLen; }
        else { os << ' '; ++lineLen; }
    }
}

std::vector<std::string> PageAbout::m_TextToLines(const std::string& text)
{
    std::vector<std::string> lines;
    std::ostringstream os;
    size_t lineLen = 0;
    auto beg = text.begin();
    while (beg != text.end())
    {
        auto ptr = beg;
        while (ptr != text.end())
        {
            if (*ptr <= 0x20) break;
            ++ptr;
        }
        m_Add_Word(lines, os, lineLen, beg, ptr, (ptr == text.end()) ? 0x00 : *ptr);
        if (ptr == text.end()) break;
        beg = ptr + 1;
    }
    if (lineLen > 0) lines.push_back(os.str());
    return lines;
}

void PageAbout::m_GetTexts(size_t& texts_Count, std::string*& texts_Title, std::string*& texts_Content)
{
    std::vector<std::string> list_Title;
    std::vector<std::string> list_Content;
    // Load about information
    char* about_Data; size_t about_Size;
    if (engine::io::IOUtil::load(FileUtil::about_Path, about_Data, about_Size))
    {
        // Parse
        char* lineBeg = about_Data;
        char* fileEnd = about_Data + about_Size;
        while (lineBeg < fileEnd)
        {
            // Look for end of line
            char* lineEnd = lineBeg;
            while (lineEnd < fileEnd) { if (*(lineEnd++) == '\n') break; }
            // Parse line
            std::string title; std::string content;
            if (m_GetTexts_ParseLine(lineBeg, lineEnd, title, content))
            {
                list_Title.push_back(std::move(title));
                list_Content.push_back(std::move(content));
            }
            // Next
            lineBeg = lineEnd;
        }
        // Cleanup
        DELETE_ARRAY(about_Data);
    }
    // Create final arrays
    texts_Count = list_Title.size();
    if (texts_Count > 0)
    {
        texts_Title = new std::string[texts_Count];
        texts_Content = new std::string[texts_Count];
        for (size_t i = 0; i < texts_Count; ++i)
        {
            texts_Title[i] = std::move(list_Title[i]);
            texts_Content[i] = std::move(list_Content[i]);
        }
    }
    else
    {
        texts_Title = nullptr;
        texts_Content = nullptr;
    }
}

bool PageAbout::m_GetTexts_ParseLine(const char* beg, const char* end, std::string& title, std::string& content)
{
    std::ostringstream os;
    // Title
    if (m_GetTexts_ReadSegment(beg, end, os))
        title = os.str();
    else return false;
    // Content
    if (m_GetTexts_ReadSegment(beg, end, os))
    {
        char* content_Data; size_t content_Size;
        if (engine::io::IOUtil::load(FileUtil::about_Dir + "/" + os.str(), content_Data, content_Size))
        {
            // Read content
            os.str(""); os.clear();
            const char* content_Ptr = content_Data;
            const char* content_End = content_Data + content_Size;
            while (content_Ptr < content_End)
                os << m_GetTexts_ReadChar(content_Ptr, content_End).value;
            content = os.str();
            // Cleanup
            DELETE_ARRAY(content_Data);
        }
        else return false;
    }
    else return false;
    // Success!!!
    return true;
}

PageAbout::Character PageAbout::m_GetTexts_ReadChar(const char*& ptr, const char* end)
{
    // Is this the end?
    if (ptr >= end) return NOCHAR;
    // Is this a regular character?
    if (*ptr != '\\') return { .value = *(ptr++), .escape = false, };
    // No! It's the start of an escape sequence.
    if (++ptr >= end) return NOCHAR;
    // Is it a simple sequence?
    switch (*ptr)
    {
        case 'n': ++ptr; return { .value = '\n', .escape = true, };
        case 't': ++ptr; return { .value = '\t', .escape = true, };
        case '\\': ++ptr; return { .value = '\\', .escape = true, };
        case '\"': ++ptr; return { .value = '\"', .escape = true, };
        case 'b': ++ptr; return { .value = '\b', .escape = true, };
        case 'r': ++ptr; return { .value = '\r', .escape = true, };
        case 'a': ++ptr; return { .value = '\a', .escape = true, };
        case '0': ++ptr; return { .value = '\0', .escape = true, };
    }
    // No! Is it an ASCII/Unicode sequence?
    char count;
    switch (*ptr)
    {
        case 'x': count = 2; break;
        case 'u': count = 4; break;
        case '_': count = 0; break;
    }
    if (count == 0) return NOCHAR;
    ++ptr;
    // Yes! Now parse.
    char chr = 0;
    while (count > 0)
    {
        if (ptr >= end) break;
        else if (*ptr >= '0' && *ptr <= '9') { chr <<= 4; chr |= *(ptr++) - '0'; }
        else if (*ptr >= 'A' && *ptr <= 'F') { chr <<= 4; chr |= 10 + (*(ptr++) - 'A'); }
        else if (*ptr >= 'a' && *ptr <= 'f') { chr <<= 4; chr |= 10 + (*(ptr++) - 'a'); }
        else break;
        --count;
    }
    return { .value = chr, .escape = true, };
}
        
bool PageAbout::m_GetTexts_ReadSegment(const char*& ptr, const char* end, std::ostringstream& os)
{
    // Look for quote
    const char* seg_beg = nullptr;
    while (ptr < end)
    {
        Character chr = m_GetTexts_ReadChar(ptr, end);
        if (chr.escape || chr.value != '\"') continue;
        seg_beg = ptr;
        break;
    }
    if (!seg_beg) return false;
    // Clear stream
    os.str(""); os.clear();
    // Look for end quote
    const char* seg_end = nullptr;
    while (ptr < end)
    {
        const char* p = ptr;
        Character chr = m_GetTexts_ReadChar(ptr, end);
        if (chr.escape || chr.value != '\"') { os << chr.value; continue; }
        seg_end = p;
        break;
    }
    if (!seg_end) return false;
    // Success!!!
    return true;
}

u8 PageAbout::m_GetTouched(u16 tile_X, u16 tile_Y, 
    const u16* btns_X, const u16* btns_Y, u16 btns_W, u16 btns_H, u8 btns_Count)
{
    for (u8 i = 0; i < btns_Count; ++i)
    {
        u16 x = btns_X[i];
        u16 y = btns_Y[i];
        if (tile_X < x) continue;
        if (tile_Y < y) continue;
        if ((tile_X - x) >= btns_W) continue;
        if ((tile_Y - y) >= btns_H) continue;
        return i;
    }
    return 0xFF;
}

void PageAbout::m_Refresh()
{
    u16* optr;
    // Title
    std::copy(f_ScreenT, f_ScreenT + f_Msg_Beg, scene().titleGFX().bg_Buffer());
    optr = scene().titleGFX().bg_Buffer() + ass::MenuAboutT::title_x + ass::MenuAboutT::title_y * DS_SCREEN_COLS;
    for (size_t i = 0; i < f_Title.length(); ++i)
    {
        if (i >= ass::MenuAboutT::title_len) break;
        *(optr++) = f_Title[i];
    }
    // Content
    if (f_Content)
    {
        u16* beg = f_Content + f_View_Offset * DS_SCREEN_COLS;
        u16* mid = beg + (DS_SCREEN_TOTAL - f_Msg_Beg);
        // Set text
        std::copy(beg, mid, scene().titleGFX().bg_Buffer() + f_Msg_Beg);
        std::copy(mid, mid + f_Msg_End, scene().textGFX().bg_Buffer());
    }
    else
    {
        std::fill(scene().titleGFX().bg_Buffer() + f_Msg_Beg, scene().titleGFX().bg_Buffer() + f_ScreenB_Len, (u16)0);
        std::fill(scene().textGFX().bg_Buffer(), scene().textGFX().bg_Buffer() + f_Msg_End, (u16)0);
    }
    // Mark dirty
    scene().titleGFX().markDirty();
    scene().textGFX().markDirty();
    // Refresh buttons
    m_Refresh_Buttons();
}

void PageAbout::m_Refresh_Buttons()
{
    u16 off;
    // Reset tiles
    off = ass::MenuAboutB::msg_end * DS_SCREEN_COLS;
    std::copy(f_ScreenB + off, f_ScreenB + f_ScreenB_Len, scene().textGFX().bg_Buffer() + off);
    // Fix page up text
    if (f_View_Offset == 0)
    {
        off = (ass::MenuAboutB::tchbtns_x[0] + ass::MenuAboutB::tchbtns_text_x) +
            (ass::MenuAboutB::tchbtns_y[0] + ass::MenuAboutB::tchbtns_text_y) * DS_SCREEN_COLS;
        std::fill(
            scene().textGFX().bg_Buffer() + off,
            scene().textGFX().bg_Buffer() + off + ass::MenuAboutB::tchbtns_text_len,
            (u16)0);
    }
    // Fix page down text
    if ((f_View_Offset + f_Msg_Height) >= f_Content_Height)
    {
        off = (ass::MenuAboutB::tchbtns_x[1] + ass::MenuAboutB::tchbtns_text_x) +
            (ass::MenuAboutB::tchbtns_y[1] + ass::MenuAboutB::tchbtns_text_y) * DS_SCREEN_COLS;
        std::fill(
            scene().textGFX().bg_Buffer() + off,
            scene().textGFX().bg_Buffer() + off + ass::MenuAboutB::tchbtns_text_len,
            (u16)0);
    }
    // Fix prev button
    if (f_TextIndex == 0)
    {
        scene().textGFX().setCursor(
            ass::MenuAboutB::buttons_x[0] + ass::MenuAboutB::buttons_text_x,
            ass::MenuAboutB::buttons_y[0] + ass::MenuAboutB::buttons_text_y);
        scene().textStream() << "     Back     ";
        scene().textStream().flush();
    }
    // Fix next button
    if ((f_TextIndex + 1) >= f_Texts_Count)
    {
        scene().textGFX().setCursor(
            ass::MenuAboutB::buttons_x[1] + ass::MenuAboutB::buttons_text_x,
            ass::MenuAboutB::buttons_y[1] + ass::MenuAboutB::buttons_text_y);
        scene().textStream() << "     Done     ";
        scene().textStream().flush();
    }
    // Highlight touch button
    if (f_Touching && f_Tch_Index < ass::MenuAboutB::tchbtns_count)
    {
        u16* beg = scene().textGFX().bg_Buffer() + 
            ass::MenuAboutB::tchbtns_x[f_Tch_Index] + 
            ass::MenuAboutB::tchbtns_y[f_Tch_Index] * DS_SCREEN_COLS;
        for (u16 y = 0; y < ass::MenuAboutB::tchbtns_h; ++y)
        {
            u16* ptr = beg;
            for (u16 x = 0; x < ass::MenuAboutB::tchbtns_w; ++x)
            {
                *ptr |= 0x2 << 12; ++ptr;
            }
            beg += DS_SCREEN_COLS;
        }
    }
    // Highlight button
    if (f_But_Index < ass::MenuAboutB::buttons_count)
    {
        u16* beg = scene().textGFX().bg_Buffer() + 
            ass::MenuAboutB::buttons_x[f_But_Index] + 
            ass::MenuAboutB::buttons_y[f_But_Index] * DS_SCREEN_COLS;
        u16 color = ((f_Touching && f_Tch_Touch >= ass::MenuAboutB::tchbtns_count) ? 0x02 : 0x01) << 12;
        for (u16 y = 0; y < ass::MenuAboutB::buttons_h; ++y)
        {
            u16* ptr = beg;
            for (u16 x = 0; x < ass::MenuAboutB::buttons_w; ++x)
            {
                *ptr |= color; ++ptr;
            }
            beg += DS_SCREEN_COLS;
        }
    }
    // Mark dirty
    scene().textGFX().markDirty();
}

void PageAbout::m_Close()
{
    PageMain* nextpage = new PageMain(scene());
    nextpage->deleteOnExit(true);
    scene().gotoPage(nextpage);
}

void PageAbout::m_SetContent(const std::string& text)
{
    // Split into lines
    std::vector<std::string> content = m_TextToLines(text);
    // Delete old buffer
    DELETE_ARRAY(f_Content);
    // Create new buffer
    f_Content_Height = MATH_MAX(f_Msg_Height, content.size());
    f_Content_Size = f_Content_Height * DS_SCREEN_COLS;
    f_Content = new u16[f_Content_Size];
    std::fill(f_Content, f_Content + f_Content_Size, (u16)0);
    {
        u16* row = f_Content;
        for (auto iptr = content.begin(); iptr != content.end(); ++iptr)
        {
            u16* optr = row;
            for (auto sptr = iptr->begin(); sptr != iptr->end(); ++sptr)
                *(optr++) = *sptr;
            row += DS_SCREEN_COLS;
        }
    }
    // Reset offset
    PageAbout::f_View_Offset = 0;
    // Refresh
    PageAbout::m_Refresh();
}

void PageAbout::m_ButtonAction()
{
    switch (f_But_Index)
    {
        case 0: 
            if (f_TextIndex > 0)
                m_Set_TextIndex(f_TextIndex - 1);
            else m_Close();
            break;
        case 1: 
            if ((f_TextIndex + 1) < f_Texts_Count)
                m_Set_TextIndex(f_TextIndex + 1);
            else m_Close();
            break;
    }
}

void PageAbout::m_Set_TextIndex(size_t value)
{
    if (f_TextIndex == value) return;
    f_TextIndex = value;
    if (f_TextIndex < f_Texts_Count)
    {
        f_Title = f_Texts_Title[f_TextIndex];
        m_SetContent(f_Texts_Content[f_TextIndex]);
    }
}

void PageAbout::m_View_Inc(size_t amount)
{
    if (!f_Content) return;
    // Set offset
    f_View_Offset += amount;
    if ((f_View_Offset + f_Msg_Height) > f_Content_Height)
        f_View_Offset = f_Content_Height - f_Msg_Height;
    // Refresh
    m_Refresh();
}

void PageAbout::m_View_Dec(size_t amount)
{
    if (!f_Content) return;
    // Set offset
    if (f_View_Offset < amount) f_View_Offset = 0;
    else f_View_Offset -= amount;
    // Refresh
    m_Refresh();
}

void PageAbout::m_PageNav()
{
    switch (f_Tch_Index)
    {
        case 0: m_View_Dec(f_Msg_Height); break;
        case 1: m_View_Inc(f_Msg_Height); break;
    }
}

#pragma endregion