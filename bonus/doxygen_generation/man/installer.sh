#!/bin/bash
##
## EPITECH PROJECT, 2024
## my_zappy
## File description:
## installer.sh
##

# Boolean data
TRUE=1
FALSE=0
DEBUG=$FALSE

# This is a simple python program that take the standard input and an output file and then write the input to the file under the correct format
PYTHON_ENCODER="/tmp/file_charset_changer.py"

# Man pages meta-data
EMAIL='<henrysoftwarehouse@protonmail\&.com>'

# SPECIAL_CHARACTERS
SC_BACKSLASH='\'
SC_QUOTE='"'
SC_DASH="${SC_BACKSLASH}-"

# Man pages known commands
M_COMMENT=".${SC_BACKSLASH}${SC_QUOTE}"

# Man Styles Inline
MSI_BOLD="${SC_BACKSLASH}fB"
MSI_RESET="${SC_BACKSLASH}fR"
MSI_COMMA="${SC_BACKSLASH},"

# Man file manager
MF_NEWLINE='\n'

function decho {
    if [ $DEBUG -eq $TRUE ]; then
        echo "$1"
    fi
}

function count_files_in_man_folder {
    decho "Counting files in man folder" >&2
    DIRECTORY="$1"/*.3
    FILE_COUNT=$(ls -1 $DIRECTORY 2>/dev/null | wc -l)
    decho "File count: $FILE_COUNT" >&2
    echo "$FILE_COUNT"
}

function dump_python_charset_changer_for_file {
    decho "Creating file charset changer"
    echo '#!/bin/env python3' >"$PYTHON_ENCODER"
    echo '# Import the sys package in order to get the standard input' >>"$PYTHON_ENCODER"
    echo 'import sys' >>"$PYTHON_ENCODER"
    echo 'error = 1  # The status when the program fails' >>"$PYTHON_ENCODER"
    echo 'success = 0  # The status when the program succeeds' >>"$PYTHON_ENCODER"
    echo 'argc = len(sys.argv)' >>"$PYTHON_ENCODER"
    echo '# Check if the argument count is not equal to 2 or (if the argument count is equal to 2 check that the content corresponds to a help call)' >>"$PYTHON_ENCODER"
    echo 'if argc != 2 or (argc == 2 and sys.argv[1].lower() in ("-h", "--help", "/?")):' >>"$PYTHON_ENCODER"
    echo '    # The print function displays text' >>"$PYTHON_ENCODER"
    echo '    print(f"USAGE:\n\t<stdin_data> | {sys.argv[0]} <file_name>")' >>"$PYTHON_ENCODER"
    echo '    # The print function displays text' >>"$PYTHON_ENCODER"
    echo '    print("DESCRIPTION:\n\tThis script is used in order make sure that the files written to the disk are in the correct format.")' >>"$PYTHON_ENCODER"
    echo '    # If the argument count is not 2, exit with an error' >>"$PYTHON_ENCODER"
    echo '    if argc != 2:' >>"$PYTHON_ENCODER"
    echo '        sys.exit(error)' >>"$PYTHON_ENCODER"
    echo '    # If we did not exit before, we exit with a success code' >>"$PYTHON_ENCODER"
    echo '    sys.exit(success)' >>"$PYTHON_ENCODER"
    echo '# If we passed the check sequence, we open a file with the name passed as an argument (with a few encoding parameters)' >>"$PYTHON_ENCODER"
    echo 'with open(f"{sys.argv[1]}", "w", encoding="utf-8", newline="\n") as file:' >>"$PYTHON_ENCODER"
    echo '    # We get the content piped in by the user' >>"$PYTHON_ENCODER"
    echo '    data = sys.stdin.read()' >>"$PYTHON_ENCODER"
    echo '    # We write it to a file' >>"$PYTHON_ENCODER"
    echo '    file.write(data)' >>"$PYTHON_ENCODER"
    echo '# Once the with loop is exited, the file is automatically closed' >>"$PYTHON_ENCODER"
    echo '# We display the "data is written to the file" message on the user"s screen' >>"$PYTHON_ENCODER"
    echo 'print("The data is written to the file")' >>"$PYTHON_ENCODER"
    echo "Granting execution wrights to: '$PYTHON_ENCODER'"
    chmod a+x $PYTHON_ENCODER
    chmod u+x $PYTHON_ENCODER
    chmod g+x $PYTHON_ENCODER
}

function get_files_in_man_folder {
    decho "In get file in man folder" >&2
    decho "PWD = $(pwd)" >&2
    DIRECTORY="$1"/*.3
    decho "Directory = $DIRECTORY, \$1 = $1" >&2
    if [ -z "$(ls -A $DIRECTORY 2>/dev/null)" ]; then
        echo "No .3 files found in $1"
        return
    fi
    MAN_CONTENT=""
    decho "Files found:" >&2
    # Iterate over the files in the directory and append their names to the man page
    for file in $DIRECTORY; do
        # Extract the file name and remove the ".3" extension
        filename=$(basename "$file")
        filename_without_extension="${filename%.3}"
        decho "file: '$filename_without_extension'" >&2
        # Append the file name to the man page content
        MAN_CONTENT+="\n.B ${MAN_PROG_DIR}/${filename_without_extension}\n"
        MAN_CONTENT+="\n.so ${MAN_PROG_DIR}/${filename}\n"
    done
    decho "Out of get file in man folder" >&2
    echo -e "$MAN_CONTENT"
}

function create_homepage_man {
    decho "In create homepage man" >&2
    decho "MAN_FOLDER='$4'" >&2
    local FILE_COUNT=$(count_files_in_man_folder "$4")
    local MAN_FILES=$(get_files_in_man_folder "$4")
    local HOMEPAGE="${M_COMMENT} Manpage for zappy project\n
${M_COMMENT} Contact: Henry Letellier ${EMAIL}.\n
.TH ZAPPY ${SC_QUOTE}EPITECH${SC_QUOTE} 6 ${SC_QUOTE}May 2024${SC_QUOTE} ${SC_QUOTE}Version 1.0${SC_QUOTE} ${SC_QUOTE}Zappy Manual${SC_QUOTE}\n
\n
.SH NAME\n
Zappy \\- Welcome to Zappy!\n
\n
.SH SYNOPSIS\n
.nf\n
.BI \\fB\\,zappy_ai\\ \\ \\t\\fR\\fI\\,\\-help\\fR\\ |\\ \\fR\\fI\\,\\-p\\ \\fRport\\fR\\ \\fR\\fI\\,\\-n\\ \\fRname\\fR\\ \\fR\\fI\\,\\-h\\ \\fRmachine\n
.BI \\fB\\,zappy_gui\\  \\t\\fR\\fI\\,\\-help\\fR\\ |\\ \\fR\\fI\\,\\-p\\ \\fRport\\ \\fI\\,\\-h\\ \\fRmachine\n
.BI \\fB\\,zappy_server\\t\\fR\\fI\\,\\-help\\fR\\ |\\ \\fR\\fI\\,\\-p\\ \\fRport\\ \\fR\\fI\\,\\fR\\fI\\,\\-x\\ \\fRwidth\\ \\fI\\,\\-y\\ \\fRheight\\ \\fI\\,\\-n\\ \\fRname1\\ name2\\ ...\\ \\fI\\,\\-c\\ \\fRclientsNb\\ \\fI\\,\\-f\\ \\fRfrequency\n
.fi\n
.SH DESCRIPTION\n
.nf\n
.BI \\fRThe\\ Zappy\\ project\\ is\\ a\\ multiplayer\\ simulation\\ game\\ where\\ players\\ inhabit\\ a\\ virtual\\ world\\ and\\ interact\\ with\\ each\\ other\\ and\\ their\\ environment.\n
.BI \\fRThe\\ game\\ environment\\ is\\ generated\\ by\\ a\\ server,\\ and\\ players\\ can\\ join\\ teams\\ to\\ compete\\ or\\ cooperate\\ in\\ various\\ challenges.\n
.BI \\fR\n
.BI \\fRThe\\ project\\ consists\\ of\\ three\\ main\\ components:\n
.IP \\[bu]\n
Server (zappy_server):\n
.BI \\fR\\tThis\\ component\\ generates\\ the\\ virtual\\ world\\ where\\ players\\ reside.\\\n
.BI \\fR\\tIt\\ manages\\ the\\ game\\ state,\\ including\\ the\\ terrain,\\ resources,\\ and\\ entities.\n
.BI \\fR\\tThe\\ server\\ listens\\ for\\ connections\\ from\\ clients\\ and\\ handles\\ their\\ interactions\\ within\\ the\\ world.\n
.IP \\[bu]\n
Graphical Client (zappy_gui):\n
.BI \\fR\\tRThe\\ graphical\\ client\\ provides\\ a\\ visual\\ representation\\ of\\ the\\ game\\ world.\n
.BI \\fR\\tRPlayers\\ can\\ observe\\ the\\ state\\ of\\ the\\ environment,\\ including\\ the\\ movements\\ of\\ entities\\ and\\ the\\ distribution\\ of\\ resources.\n
.BI \\fR\\tRIt\\ enhances\\ the\\ gaming\\ experience\\ by\\ offering\\ real-time\\ updates\\ and\\ immersive\\ graphics.\n
.IP \\[bu]\n
AI Client (zappy_ai):\n
.BI \\fR\\tThe\\ AI\\ client\\ allows\\ players\\ to\\ control\\ virtual\\ inhabitants\\ within\\ the\\ game\\ world.\n
.BI \\fR\\tPlayers\\ can\\ develop\\ strategies\\ and\\ algorithms\\ to\\ navigate\\ the\\ environment,\\ gather\\ resources,\\ and\\ interact\\ with\\ other\\ players.\n
.BI \\fR\\tPThe\\ AI\\ client\\ communicates\\ with\\ the\\ server\\ to\\ execute\\ commands\\ and\\ receive\\ updates\\ on\\ the\\ game\\ state.\n
.PP\n
.BI \\fRThe\\ Zappy\\ project\\ offers\\ an\\ engaging\\ and\\ collaborative\\ gaming\\ experience,\\ where\\ players\\ can\\ explore,\\ strategize,\\ and\\ compete\\ in\\ a\\ dynamic\\ virtual\\ world.\n
.fi\n
.PP\n
.SH OPTIONS\n
.nf\n
.PP\n
.BI\\,zappy_ai:\\fR\n
.BI\\t\\t\\fR\\fI\\,\\-help\n
.BI\\t\\t\\t\\fRThis\\ flag\\ will\\ display\\ the\\ help\\ for\\ this\\ binary\\ and\\ then\\ exit.\n
.BI\\t\\t\\fR\\fI\\,\\-p\\ \\fRport\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ port\\ on\\ which\\ the\\ binary\\ will\\ communicate\\ with\\ the\\ two\\ other\\ binaries.\n
.BI\\t\\t\\fR\\fI\\,\\-n\\ \\fRname\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ name\\ that\\ will\\ be\\ given\\ the\\ AI\\ process.\n
.BI\\t\\t\\fR\\fI\\,\\-h\\ \\fRmachine\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ ip\\ on\\ which\\ the\\ \\fBAI\\fR\\ is\\ to\\ talk.\\ (default:\\ localhost\\ [i.e:\\ 127.0.0.1])\n
.PP\n
.BI\\,zappy_gui:\\fR\n
.BI\\t\\t\\fR\\fI\\,\\-help\n
.BI\\t\\t\\t\\fRThis\\ flag\\ will\\ display\\ the\\ help\\ for\\ this\\ binary\\ and\\ then\\ exit.\n
.BI\\t\\t\\fR\\fI\\,\\-p\\ \\fRport\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ port\\ on\\ which\\ the\\ binary\\ will\\ communicate\\ with\\ the\\ two\\ other\\ binaries.\n
.BI\\t\\t\\fR\\fI\\,\\-h\\ \\fRmachine\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ ip\\ on\\ which\\ the\\ \\fBGUI\\fR\\ is\\ to\\ talk.\\ (default:\\ localhost\\ [i.e:\\ 127.0.0.1])\n
.PP\n
.BI\\,zappy_server:\\fR\n
.BI\\t\\t\\fR\\fI\\,\\-help\n
.BI\\t\\t\\t\\fRThis\\ flag\\ will\\ display\\ the\\ help\\ for\\ this\\ binary\\ and\\ then\\ exit.\n
.BI\\t\\t\\fR\\fI\\,\\-p\\ \\fRport\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ port\\ on\\ which\\ the\\ binary\\ will\\ communicate\\ with\\ the\\ two\\ other\\ binaries.\n
.BI\\t\\t\\fR\\fI\\,\\-x\\ \\fRwidth\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ \\fBwidth\\fR\\ of\\ the\\ world.\n
.BI\\t\\t\\fR\\fI\\,\\-y\\ \\fRheight\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ \\fBheight\\fR\\ of\\ the\\ world.\n
.BI\\t\\t\\fR\\fI\\,\\-n\\ \\fRname1\\ name2\\ ...\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ name(s)\\ of\\ the\\ team(s)\\ that\\ will\\ play.\n
.BI\\t\\t\\t\\fRMultiple\\ team\\ names\\ should\\ be\\ separated\\ by\\ spaces.\n
.BI\\t\\t\\fR\\fI\\,\\-c\\ \\fRclientsNb\n
.BI\\t\\t\\t\\fRThis\\ flag\\ specifies\\ the\\ maximum\\ number\\ of\\ clients\\ that\\ are\\ allowed\\ to\\ play.\n
.BI\\t\\t\\fR\\fI\\,\\-f\\ \\fRfrequency\n
.BI\\t\\t\\t\\fRSpecifies\\ the\\ number\\ of\\ actions\\ per\\ time\\ unit.\n
.BI\\t\\t\\t\\fRA\\ higher\\ frequency\\ means\\ actions\\ happen\\ faster.\n
.fi\n
.PP\n
.SH USAGE\n
.nf\n
.BI \\fRExample\\ usage:\n
.BI \\fRIn\\ this\\ example\\ the\\ 4\\ lines\\ need\\ to\\ be\\ run\\ one\\ after\\ the\\ other\\ (we\\ are\\ in\\ a\\ linux/mac\\ environment).\n
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4242\\ \\-n\\ team1\\ \\-h\\ localhost\\ &\n
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4243\\ \\-n\\ team2\\ \\-h\\ localhost\\ &\n
.BI \\fR\\t./zappy_server\\ \\-p\\ 4244\\ \\-x\\ 100\\ \\-y\\ 100\\ \\-n\\ team1\\ team2\\ \\-c\\ 10\\ \\-f\\ 100\\ &\n
.BI \\fR\\t./zappy_gui\\ \\-p\\ 4245\\ \\-h\\ localhost\\ &\n
.PP\n
.fi\n
.SH SEE ALSO\n
.nf\n
.BI zappy_ai(1),\\ zappy_gui(1),\\ zappy_server(1)\n
.fi\n
.SH AUTHOR\n
Written by (c) Henry Letellier.\n
.PP\n
.SH DEVELOPERS\n
.nf\n
.B (c)\\ Harleen\\ Singh-Kaur\n
.B (c)\\ Eric\\ Xu\n
.B (c)\\ Victor\\ Yvon\n
.B (c)\\ Thomas\\ Lebouc\n
.B (c)\\ Henry\\ Letellier\n
.fi\n
.PP\n
.SH COPYRIGHT\n
.nf\n
.BI \\fRThis\\ is\\ a\\ project\\ that\\ was\\ created\\ during\\ our\\ second\\ year\\ at\\ Epitech.\n
.BI \\fRThus,\\ feel\\ free\\ to\\ use\\ this\\ project,\\ but\\ you\\ cannot\\ edit,\\ sel\\ or\\ re-sel\\ it.\n
.fi\n
.PP\n
.SH BUGS\n
.nf\n
.BI \\fRPlease\\ report\\ any\\ bugs\\ to\\ ${EMAIL}.\n
.BI \\fRAlthough,\\ there\\ is\\ absolutely\\ no\\ guaranty\\ that\\ it\\ will\\ be\\ fixed.\n
.BI \\fRAnother\\ way\\ would\\ be\\ to\\ open\\ an\\ issue\\ on\\ the\\ github\\ project,\\ see\\ \"PROJECT\\ RESSOURCES\"\\ for\\ more\\ details.\n
.fi\n
.PP\n
.SH NOTES\n
.nf\n
.BI \\fIThis\\ man\\ page\\ is\\ for\\ informational\\ purposes\\ only.\n
.BI \\fRFor\\ detailed\\ usage\\ instructions,\\ please\\ refer\\ to\\ the\\ specific\\ manual\\ pages\\ listed\\ under\\ \"SEE\\ ALSO\".\n
.BI \\fRYou\\ can\\ also\\ find\\ links\\ concerning\\ the\\ project\\ in\\ \"PROJECT\\ RESSOURCES\"\n
.fi\n
.PP\n
.SH PROJECT RESSOURCES\n
.nf\n
${M_COMMENT} .BI\\fRWebsite:\\ https://zappy\\&.pingpal\\&.news/\n
.BI \\fRSource\\ code\\ (Github):\\ https://github\\&.com/Hanra-s-work/my_zappy/\n
.BI \\fRDocumentation:\\ https://zappy\\&.pingpal\\&.news/\n
.fi\n
.PP\n
.SH DISCLAIMER\n
.PP\n
This software is provided \"as is\" without warranty of any kind. Use at your own risk.\n
.PP\n
.SH VERSION\n
1.0\n
.PP\n
.SH DATE\n
May 2024\n
.PP\n
.SH SUB-PAGE DOXY DUMP [${FILE_COUNT} file(s)] (very crude for now)\n
$MAN_FILES
"
    decho "Homepage generated" >&2
    mkdir -p "$1"
    if [ $DEBUG -eq $TRUE ]; then
        echo -e "$HOMEPAGE"
    fi
    echo -e "$HOMEPAGE" | $PYTHON_ENCODER "$1/$2.$3"
}

function create_zappy_ai_man {
    decho "In create_zappy_ai_man" >&2
    decho "MAN_FOLDER='$4'" >&2
    local FILE_COUNT=$(count_files_in_man_folder "$4")
    local MAN_FILES=$(get_files_in_man_folder "$4")
    local HOMEPAGE="${M_COMMENT} Manpage for zappy project\n
${M_COMMENT} Contact: Henry Letellier ${EMAIL}.\n
.TH ZAPPY \"ZAPPY_AI EPITECH\" 1 \"May 2024\" \"Version 1.0\" \"Zappy Manual \\- ZAPPY_AI\"\n
.SH NAME\n
.BI \\fBzappy_ai\\ \\-\\ binary\\ in\\ charge\\ of\\ driving\\ the\\ inhabitants\\ through\\ orders\\ sent\\ to\\ the\\ server\\ binary.\n
.PP\n
.SH SYNOPSIS\n
.nf\n
.BI \\fB\,zappy_ai\\ \\ \\t\\fR\\fI\,\\-help\\fR\\ |\\ \\fR\\fI\,\-p\\ \\fRport\\fR\\ \\fR\\fI\,\\-n\\ \\fRname\\fR\\ \\fR\\fI\,\\-h\\ \\fRmachine\n
.fi\n
.PP\n
.SH DESCRIPTION\n
.nf\n
.BI \\fRzappy_ai\\ is\\ a\\ binary\\ used\\ to\\ control\\ an\\ inhabitant\\ in\\ the\\ world\\ generated\\ by\\ the\\ zappy_server.\n
.BI \\fRIt\\ sends\\ orders\\ to\\ the\\ server\\ to\\ interact\\ with\\ the\\ world.\n
.fi\n
.PP\n
.SH OPTIONS\n
.nf\n
.BI \\fR\\-p\\ PORT\n
.BI \\fR\\tSpecifies\\ the\\ port\\ number\\ to\\ connect\\ to.\n
.PP\n
.BI \\fR\\-n\\ TEAM_NAME\n
.BI \\fR\\tSpecifies\\ the\\ name\\ of\\ the\\ team.\n
.PP\n
.BI \\fR\\-h\\ HOST\n
.BI \\fR\\tSpecifies\\ the\\ hostname\\ of\\ the\\ machine\\ to\\ connect\\ to.\n
.BI \\fR\\tDefaults\\ to\\ localhost\\ if\\ not\\ specified.\n
.fi\n
.PP\n
.SH USAGE\n
.nf\n
.BI \\fRExample\\ usage:\n
.BI \\fRIn\\ this\\ example\\ the\\ 4\\ lines\\ need\\ to\\ be\\ run\\ one\\ after\\ the\\ other\\ (we\\ are\\ in\\ a\\ linux/mac\\ environment).\n
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4242\\ \\-n\\ team1\\ \\-h\\ localhost\\ &\n
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4243\\ \\-n\\ team2\\ \\-h\\ localhost\\ &\n
.BI \\fR\\t./zappy_server\\ \\-p\\ 4244\\ \\-x\\ 100\\ \\-y\\ 100\\ \\-n\\ team1\\ team2\\ \\-c\\ 10\\ \\-f\\ 100\\ &\n
.BI \\fR\\t./zappy_gui\\ \\-p\\ 4245\\ \\-h\\ localhost\\ &\n
.fi\n
.PP\n
.SH REPORTING BUGS\n
.BI \\fRReport\\ bugs\\ to\\ ${EMAIL}.\n
.PP\n
.SH COPYRIGHT\n
.nf\n
.BI \\fRThis\\ is\\ a\\ project\\ that\\ was\\ created\\ during\\ our\\ second\\ year\\ at\\ Epitech.\n
.BI \\fRThus,\\ feel\\ free\\ to\\ use\\ this\\ project,\\ but\\ you\\ cannot\\ edit,\\ sel\\ or\\ re-sel\\ it.\n
.fi\n
.PP\n
.SH PROJECT RESSOURCES\n
.nf\n
${M_COMMENT} .BI\\fRWebsite:\\ https://zappy\\&.pingpal\\&.news/\n
.BI \\fRSource\\ code\\ (Github):\\ https://github\\&.com/Hanra-s-work/my_zappy/\n
.BI \\fRDocumentation:\\ https://zappy\\&.pingpal\\&.news/\n
.fi\n
.PP\n
.SH VERSION\n
1.0\n
.PP\n
.SH DATE\n
May 2024\n
.SH AUTHOR\n
Written by (c) Henry Letellier.\n
.PP\n
.SH DEVELOPERS\n
.nf\n
.B (c)\\ Harleen\\ Singh-Kaur\n
.B (c)\\ Eric\\ Xu\n
.B (c)\\ Victor\\ Yvon\n
.B (c)\\ Thomas\\ Lebouc\n
.B (c)\\ Henry\\ Letellier\n
.fi\n
.PP\n
.SH SEE ALSO\n
.nf\n
.BI zappy(6),\\ zappy_gui(1),\\ zappy_server(1)\n
.fi\n
.SH SUB-PAGE DOXY DUMP [${FILE_COUNT} file(s)] (very crude for now)\n
$MAN_FILES
"
    decho "Homepage generated" >&2
    mkdir -p "$1"
    if [ $DEBUG -eq $TRUE ]; then
        echo -e "$HOMEPAGE"
    fi
    echo -e "$HOMEPAGE" | $PYTHON_ENCODER "$1/$2.$3"

}

function create_zappy_gui_man {
    decho "In create_zappy_gui_man" >&2
    decho "MAN_FOLDER='$4'" >&2
    local FILE_COUNT=$(count_files_in_man_folder "$4")
    local MAN_FILES=$(get_files_in_man_folder "$4")
    local HOMEPAGE="${M_COMMENT} Manpage for zappy project\n
${M_COMMENT} Contact: Henry Letellier <henrysoftwarehouse@protonmail.com>.\n
.TH ZAPPY \"ZAPPY_GUI EPITECH\" 1 \"May 2024\" \"Version 1.0\" \"Zappy Manual \\- ZAPPY_GUI\"\n
.SH NAME\n
.PP\n
.NAME\n
.BI \\fBzappy_gui\\ \\-\\ graphical\\ client\\ to\\ watch\\ the\\ inhabitants'\\ world\n
.PP\n
.SH SYNOPSIS\n
.nf\n
.BI \\fB\\,zappy_gui\\  \\t\\fR\\fI\\,\\-help\\fR\\ |\\ \\fR\\fI\\,\\-p\\ \\fRport\\ \\fI\\,\\-h\\ \\fRmachine\n
.fi\n
.PP\n
.SH DESCRIPTION\n
.nf\n
.BI \\fRzappy_gui\\ is\\ a\\ graphical\\ client\\ used\\ to\\ visualize\\ the\\ state\\ of\\ the\\ inhabitants'\\ world\\ and\\ the\\ actions\\ occurring\\ within\\ it.\n
.PP\n
.fi\n
.SH OPTIONS\n
.nf\n
.BI \\fR\\-p\\ PORT\n
.BI \\fR\\tSpecifies\\ the\\ port\\ number\\ to\\ connect\\ to.\n
.PP\n
.BI \\fR\\-h\\ HOST\n
.BI \\fR\\tSpecifies\\ the\\ hostname\\ of\\ the\\ machine\\ to\\ connect\\ to.\n
.fi\n
.PP\n
.SH USAGE\n
.nf\n
.BI \\fRExample\\ usage:\n
.BI \\fRIn\\ this\\ example\\ the\\ 4\\ lines\\ need\\ to\\ be\\ run\\ one\\ after\\ the\\ other\\ (we\\ are\\ in\\ a\\ linux/mac\\ environment).\n
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4242\\ \\-n\\ team1\\ \\-h\\ localhost\\ &\n
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4243\\ \\-n\\ team2\\ \\-h\\ localhost\\ &\n
.BI \\fR\\t./zappy_server\\ \\-p\\ 4244\\ \\-x\\ 100\\ \\-y\\ 100\\ \\-n\\ team1\\ team2\\ \\-c\\ 10\\ \\-f\\ 100\\ &\n
.BI \\fR\\t./zappy_gui\\ \\-p\\ 4245\\ \\-h\\ localhost\\ &\n
.fi\n
.PP\n
.SH REPORTING BUGS\n
.BI \\fRReport\\ bugs\\ to\\ <henrysoftwarehouse@protonmail\\&.com>.\n
.PP\n
.SH COPYRIGHT\n
.nf\n
.BI \\fRThis\\ is\\ a\\ project\\ that\\ was\\ created\\ during\\ our\\ second\\ year\\ at\\ Epitech.\n
.BI \\fRThus,\\ feel\\ free\\ to\\ use\\ this\\ project,\\ but\\ you\\ cannot\\ edit,\\ sel\\ or\\ re-sel\\ it.\n
.fi\n
.PP\n
.SH PROJECT RESSOURCES\n
.nf\n
${M_COMMENT} .BI\\fRWebsite:\\ https://zappy\\&.pingpal\\&.news/\n
.BI \\fRSource\\ code\\ (Github):\\ https://github\\&.com/Hanra-s-work/my_zappy/\n
.BI \\fRDocumentation:\\ https://zappy\\&.pingpal\\&.news/\n
.fi\n
.PP\n
.SH DISCLAIMER\n
.PP\n
This software is provided \"as is\" without warranty of any kind. Use at your own risk.\n
.PP\n
.SH VERSION\n
1.0\n
.PP\n
.SH DATE\n
May 2024\n
.SH AUTHOR\n
Written by (c) Henry Letellier.\n
.PP\n
.SH DEVELOPERS\n
.nf\n
.B (c)\\ Harleen\\ Singh-Kaur\n
.B (c)\\ Eric\\ Xu\n
.B (c)\\ Victor\\ Yvon\n
.B (c)\\ Thomas\\ Lebouc\n
.B (c)\\ Henry\\ Letellier\n
.fi\n
.PP\n
.SH SEE ALSO\n
.nf\n
.BI zappy(6),\\ zappy_server(1),\\ zappy_ai(1)\n
.fi\n
.PP\n
.SH SUB-PAGE DOXY DUMP [${FILE_COUNT} file(s)] (very crude for now)\n
$MAN_FILES
"
    decho "Homepage generated" >&2
    mkdir -p "$1"
    if [ $DEBUG -eq $TRUE ]; then
        echo -e "$HOMEPAGE"
    fi
    echo -e "$HOMEPAGE" | $PYTHON_ENCODER "$1/$2.$3"

}

function create_zappy_server_man {
    decho "In create_zappy_server_man" >&2
    decho "MAN_FOLDER='$4'" >&2
    FILE_COUNT=$(count_files_in_man_folder "$4")
    MAN_FILES=$(get_files_in_man_folder "$4")
    HOMEPAGE="${M_COMMENT} Manpage for zappy project\n
${M_COMMENT} Contact: Henry Letellier <henrysoftwarehouse@protonmail.com>.\n
.TH ZAPPY ${SC_QUOTE}ZAPPY_SERVER EPITECH${SC_QUOTE} 1 ${SC_QUOTE}May 2024${SC_QUOTE} ${SC_QUOTE}Version 1.0${SC_QUOTE} ${SC_QUOTE}Zappy Manual \\- ZAPPY_GUI${SC_QUOTE}
.SH NAME
.BI\\ \\fBzappy_server\\ \\-\\ generate\\ the\\ inhabitants’\\ world
.PP
.SH SYNOPSIS
.BI \\fB\,zappy_server\\t\\fR\\fI\,\\-help\\fR\\ |\\ \\fR\\fI\,\\-p\\ \\fRport\\ \\fR\\fI\,\\fR\\fI\,\\-x\\ \\fRwidth\\ \\fI\,\\-y\\ \\fRheight\\ \\fI\,\\-n\\ \\fRname1\\ name2\\ ...\\ \\fI\,\\-c\\ \\fRclientsNb\\ \\fI\,\\-f\\ \\fRfrequency
.PP
.SH DESCRIPTION
.BI \\fRzappy_server\\ generates\\ a\\ world\\ for\\ inhabitants\\ to\\ live\\ in\\ and\\ interact.
.PP
.SH OPTIONS
.BI \\fR\\-p\\ PORT
.BI \\fR\tSpecifies\\ the\\ port\\ number\\ on\\ which\\ the\\ server\\ listens.
.PP
.BI \\fR\\-x\\ WIDTH
.BI \\fR\tSpecifies\\ the\\ width\\ of\\ the\\ world.
.PP
.BI \\fR\\-y\\ HEIGHT
.BI \\fR\tSpecifies\\ the\\ height\\ of\\ the\\ world.
.PP
.BI \\fR\\-n\\ TEAM_NAMES
.BI \\fR\tSpecifies\\ the\\ names\\ of\\ the\\ teams.\\ Multiple\\ team\\ names\\ should\\ be\\ separated\\ by\\ spaces.
.PP
.BI \\fR\\-c\\ CLIENTS_NUMBER
.BI \\fR\tSpecifies\\ the\\ number\\ of\\ authorized\\ clients\\ per\\ team.
.PP
.BI \\fR\\-f\\ FREQUENCY
.BI \\fR\tSpecifies\\ the\\ reciprocal\\ of\\ the\\ time\\ unit\\ for\\ the\\ execution\\ of\\ actions.
.PP
.SH USAGE
.nf
.BI \\fRExample\\ usage:
.BI \\fRIn\\ this\\ example\\ the\\ 4\\ lines\\ need\\ to\\ be\\ run\\ one\\ after\\ the\\ other\\ (we\\ are\\ in\\ a\\ linux/mac\\ environment).
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4242\\ \\-n\\ team1\\ \\-h\\ localhost\\ &
.BI \\fR\\t./zappy_ai\\ \\-p\\ 4243\\ \\-n\\ team2\\ \\-h\\ localhost\\ &
.BI \\fR\\t./zappy_server\\ \\-p\\ 4244\\ \\-x\\ 100\\ \\-y\\ 100\\ \\-n\\ team1\\ team2\\ \\-c\\ 10\\ \\-f\\ 100\\ &
.BI \\fR\\t./zappy_gui\\ \\-p\\ 4245\\ \\-h\\ localhost\\ &
.PP
.fi
.SH AUTHOR
Written by (c) Henry Letellier.
.PP
.SH COPYRIGHT
.nf
.BI \\fRThis\\ is\\ a\\ project\\ that\\ was\\ created\\ during\\ our\\ second\\ year\\ at\\ Epitech.
.BI \\fRThus,\\ feel\\ free\\ to\\ use\\ this\\ project,\\ but\\ you\\ cannot\\ edit,\\ sel\\ or\\ re-sel\\ it.
.fi
.PP
.SH BUGS
.nf
.BI \\fRPlease\\ report\\ any\\ bugs\\ to\\ <henrysoftwarehouse@protonmail\&.com>.
.BI \\fRAlthough,\\ there\\ is\\ absolutely\\ no\\ guaranty\\ that\\ it\\ will\\ be\\ fixed.
.BI \\fRAnother\\ way\\ would\\ be\\ to\\ open\\ an\\ issue\\ on\\ the\\ github\\ project,\\ see\\ \"PROJECT\\ RESSOURCES\"\\ for\\ more\\ details.
.fi
.PP
.SH NOTES
.nf
.BI \\fIThis\\ man\\ page\\ is\\ for\\ informational\\ purposes\\ only.
.BI \\fRFor\\ detailed\\ usage\\ instructions,\\ please\\ refer\\ to\\ the\\ specific\\ manual\\ pages\\ listed\\ under\\ \"SEE\\ ALSO\".
.BI \\fRYou\\ can\\ also\\ find\\ links\\ concerning\\ the\\ project\\ in\\ \"PROJECT\\ RESSOURCES\"
.fi
.PP
.SH PROJECT RESSOURCES
.nf
${M_COMMENT} .BI\\fRWebsite:\\ https://zappy\\&.pingpal\\&.news/
.BI \\fRSource\\ code\\ (Github):\\ https://github\\&.com/Hanra-s-work/my_zappy/
.BI \\fRDocumentation:\\ https://zappy\\&.pingpal\\&.news/
.fi
.PP
.SH DISCLAIMER
.PP
This software is provided ${SC_QUOTE}as is${SC_QUOTE} without warranty of any kind. Use at your own risk.
.PP
.SH VERSION
1.0
.PP
.SH DATE
May 2024
.PP
.SH DEVELOPERS
.nf
.B (c)\\ Harleen\\ Singh-Kaur
.B (c)\\ Eric\\ Xu
.B (c)\\ Victor\\ Yvon
.B (c)\\ Thomas\\ Lebouc
.B (c)\\ Henry\\ Letellier
.fi
.PP
.SH SEE ALSO
.nf
.BI zappy(6),\\ zappy_ai(1),\\ zappy_gui(1)
.fi
.SH SUB-PAGE DOXY DUMP [${FILE_COUNT} file(s)] (very crude for now)\n
$MAN_FILES
"
    decho "Homepage generated" >&2
    mkdir -p "$1"
    if [ $DEBUG -eq $TRUE ]; then
        echo -e "$HOMEPAGE"
    fi
    echo -e "$HOMEPAGE" | $PYTHON_ENCODER "$1/$2.$3"

}

function update_man_paths {
    MAN_DEST="$1"
    # Update the shell man paths to include the zappy folder
    echo "Updating the shell man paths to include the zappy folder"
    export MANPATH="/usr/local/man:/usr/local/share/man:/usr/share/man:$MAN_DEST:$MANPATH"
    SHELL_PATHS=("/etc/bash.bashrc" "/etc/bashrc" "/etc/profile" "/etc/zsh/zshenv" "/etc/zshrc" "/etc/fish/config.fish")

    SHELL_LINE="export MANPATH=\"/usr/local/man:/usr/local/share/man:/usr/share/man:$MAN_DEST:\$MANPATH\""
    for i in "${SHELL_PATHS[@]}"; do
        # Check if the line is already present in the file
        if ! grep -qF "$SHELL_LINE" "$i"; then
            echo "$SHELL_LINE" >>"$i"
            decho "Added MANPATH to '$i'"
        else
            decho "MANPATH is already present in '$i' not adding"
        fi
    done
    echo "Updated the shell man paths to include the zappy folder"
}

function add_required_mans {
    MAN_DEST="$2"
    MAN_DIR="$1"
    shift 2
    MANS=("$@")
    # Create a symbolic link for the main man page
    for i in "${MANS[@]}"; do
        MAN_FILE="$i" #"${i%.*}"
        if [ ! -L "$MAN_DEST/$i" ]; then
            echo "Creating symbolic link of '$MAN_DEST/$i' to '$MAN_DIR/$MAN_FILE'"
            ln -sf "$MAN_DEST/$i" "$MAN_DIR/$MAN_FILE"
            STATUS=$?
            if [ $STATUS -ne 0 ]; then
                echo "This operation failed, please re-run this program with -d or do the operation manually"
                exit $STATUS
            fi
            echo "Symbolic link created of '$MAN_DEST/$i' to '$MAN_DIR/$MAN_FILE'"
        else
            echo "A symbolic link of '$MAN_DEST/$i' to '$MAN_DIR/$MAN_FILE' already exists"
        fi
    done
}

function update_man_db {
    MY_MAN_PATH="$1"
    DESTINATION="$2"
    PROJECT_DIRECTORY="$3"
    if [ "$MY_MAN_PATH" = "" ]; then
        echo "Argument 1 cannot be empty (update man db)"
        return
    fi
    if grep -qF "$MY_MAN_PATH" "$DESTINATION"; then
        echo "The man paths for zappy are correct"
        return
    fi
    echo "#" >>"$DESTINATION"
    echo "#---------------------------------------------------------" >>"$DESTINATION"
    echo "# These are injections so that the '$PROJECT_DIRECTORY' man works properly" >>"$DESTINATION"
    echo "# Adding '$PROJECT_DIRECTORY' to the search path of the man so that you can do man '$PROJECT_DIRECTORY/child_element'" >>"$DESTINATION"
    decho "# Adding '$PROJECT_DIRECTORY' to the search path of the man so that you can do man '$PROJECT_DIRECTORY/child_element'"
    echo "MANDATORY_MANPATH			$MY_MAN_PATH" >>"$DESTINATION"
    decho "# Adding '$PROJECT_DIRECTORY' to the user specifiable targets"
    sed -i "s/^SECTION.*/& $PROJECT_DIRECTORY/" "$DESTINATION"
    echo "The man db file has been updated"
}

function update_database {
    # Update the man database
    echo "Updating database"
    mandb
    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "This operation failed, please re-run this program with -d or do the operation manually"
        exit $STATUS
    fi
    echo "Database updated"
}

function display_help() {
    echo "USAGE:"
    echo "       $0   [-h|--help|-d]"
    echo "PARAMETERS:"
    echo "       -h or --help is to display this help section"
    echo "       -d or --debug is to enable a debug display of the program"
}

# Check if administrator
if [ $# -ge 2 ]; then
    display_help
    exit 1
fi

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    display_help
    exit 0
fi

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    sudo $0 $@
    exit $?
fi

if [ "$1" == "-d" ] || [ "$1" == "--debug" ]; then
    DEBUG=$TRUE
else
    DEBUG=$FALSE
fi

# Define the installation directory for man pages
UPDATE_DB_FILE=$TRUE
MAN_DIR="/usr/share/man/"
MAN_PROG_DIR="zappy"
MAN_DEST="${MAN_DIR}${MAN_PROG_DIR}"
MAN_LEVEL=6
MAN_SHORTCUT_HOME="${MAN_DIR}man${MAN_LEVEL}"
MAN_SHORTCUT_BINS="${MAN_DIR}man1"
MAN_SOURCE="./man6"
MAN_DB="/etc/man_db.conf"

# Create a python file that will be used to change the file encoding of the man pages we are going to create
# See function content for line by line comments
dump_python_charset_changer_for_file

# Removing existing man pages if they exist
echo "Removing previous manual entries of this program if they existed"
decho "Removing '$MAN_DEST' entry if it exists"
if [ $DEBUG -eq $TRUE ]; then
    rm -rvf "$MAN_DEST"
else
    rm -rf "$MAN_DEST"
fi
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
decho "Removing '${MAN_SHORTCUT_HOME}/${MAN_PROG_DIR}.${MAN_LEVEL}' if it exists"
if [ $DEBUG -eq $TRUE ]; then
    rm -vf "${MAN_SHORTCUT_HOME}/${MAN_PROG_DIR}.${MAN_LEVEL}"
else
    rm -f "${MAN_SHORTCUT_HOME}/${MAN_PROG_DIR}.${MAN_LEVEL}"
fi
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
decho "Removed '$MAN_DEST' and '$MAN_DIR/zappy.3' is they existed"
echo "Previous entries, if present, have been removed"

# Create the directory structure for your project's man pages
decho "Creating folder '$MAN_DEST'"
mkdir -p "$MAN_DEST"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
decho "Created folder '$MAN_DEST'"

# Copy or move your man pages into the appropriate directory
echo "Copying contents from the data folder to the man folder"
cd $MAN_SOURCE
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
if [ $DEBUG -eq $TRUE ]; then
    cp -rvf * "$MAN_DEST"
else
    cp -rf * "$MAN_DEST"
fi
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
cd ..
echo "Content of '$MAN_SOURCE' has been copied to '$MAN_DEST'"

# Creating the homepage
echo "Generating homepage"
create_homepage_man "$MAN_DEST" "$MAN_PROG_DIR" "$MAN_LEVEL" "$MAN_SOURCE"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
echo "Homepage has been generated"
echo "Generating page zappy_ai"
create_zappy_ai_man "$MAN_DEST" "zappy_ai" "1" "$MAN_SOURCE"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
echo "zappy_ai page has been generated"
echo "Generating page zappy_gui"
create_zappy_gui_man "$MAN_DEST" "zappy_gui" "1" "$MAN_SOURCE"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
echo "zappy_gui page has been generated"
echo "Generating page zappy_server"
create_zappy_server_man "$MAN_DEST" "zappy_server" "1" "$MAN_SOURCE"
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "This operation failed, please re-run this program with -d or do the operation manually"
    exit $STATUS
fi
echo "zappy_server page has been generated"

echo "Adding required man links"
add_required_mans "$MAN_SHORTCUT_HOME" "$MAN_DEST" "zappy.6"
add_required_mans "$MAN_SHORTCUT_BINS" "$MAN_DEST" "zappy_ai.1" "zappy_gui.1" "zappy_server.1"
echo "Added required man links"

if [ "$UPDATE_DB_FILE" = "$TRUE" ]; then
    decho "You chose to update the db file"
    update_man_db "$MAN_DEST" "$MAN_DB" "$MAN_PROG_DIR"
else
    decho "You chose to use the MANPATH environment variable"
    update_man_paths "$MAN_DEST"
fi

update_database

echo "Installation complete. You can now use 'man zappy' to access the manual page."
echo "Please relaunch any terminal instances you have for the full effect of the new man pages to be applied"

echo "(C) Created by Henry Letellier"
echo "This program is provided as if and without any warranty"
