%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% NAME:             designdoc.cls
%
% AUTHOR:           Ethan D. Twardy <edtwardy@mtu.edu>
%
% DESCRIPTION:      LaTeX class file for design documents.
%
% CREATED:          05/15/2019
%
% LAST EDITED:      07/17/2020
%%%

\LoadClass[12pt]{article}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{designdoc}[2019/05/15 Class for Software Design Documents]

\pagestyle{empty} % Prevent style conflicts with `fancy'
\RequirePackage[margin=1in]{geometry} % Pretty much just to set the margins
\RequirePackage{fancyhdr} % Header & Footer
\RequirePackage{setspace} % Spacing.
\RequirePackage{graphicx}
\RequirePackage{relsize}
\RequirePackage{algorithm}
\RequirePackage[noend]{algpseudocode}
\RequirePackage{minted}
\RequirePackage{amsmath}
\RequirePackage{hyperref}
\RequirePackage{tabularx}
\RequirePackage{fmtcount}
\RequirePackage[T1]{fontenc} % Use Computer Modern font
\RequirePackage{titlesec}

\ifpdf
\RequirePackage{Alegreya}
\RequirePackage{AlegreyaSans}
\fi

\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  urlcolor=cyan
}

% Header
\setlength{\headheight}{28pt}
\pagestyle{fancy}
\fancyhf{}
\rhead{Ethan D. Twardy}
\lhead{SortMedia Design Document}

\newcommand{\expnumber}[2]{{#1}\mathrm{e}{#2}}

\setlength{\parskip}{10pt}
\setlength{\parindent}{0pt}

% Custom titleing
\makeatletter
\renewcommand{\maketitle}{
  {\Huge\sffamily\bfseries\@title\normalsize\vspace{1em}\\\large\@author%
    \\\normalsize\@date}
}
\makeatother

% Custom sectioning
\titlespacing*{\section}{0pt}{1em}{0pt}
\titlespacing*{\subsection}{0pt}{1em}{0pt}
\titleformat*{\section}{\LARGE\sffamily\bfseries}
\titleformat*{\subsection}{\Large\sffamily\bfseries}

\newcommand{\answer}[1]{
  \begin{enumerate}
  \item[] #1
  \end{enumerate}
}

\newsavebox{\mybox}
\newenvironment{Answer}%
{\par\begin{lrbox}{\mybox}\begin{minipage}{\linewidth-7pt}}
{\end{minipage}\end{lrbox}\fbox{\usebox{\mybox}}}

\newcounter{TheRequirement}
\newcounter{reqpadding}
\setcounter{reqpadding}{4}
\newcommand{\swrequirement}[1]{
  \stepcounter{TheRequirement}
  \subsection*{SR\padzeroes[\value{reqpadding}]{\decimal{TheRequirement}}: #1}
}

\usemintedstyle{solarized-dark}
\setminted{fontsize=\normalsize}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
