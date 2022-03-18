%%% 

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ca-conf}
                [2010/08/02 v0.1.0
                Caomputer Algebra Conference]

\ExecuteOptions{a4paper,10pt,twoside,onecolumn,final,openany}
\ProcessOptions*\relax

\LoadClassWithOptions{kproc}

% \AtBeginDocument{%
%   \pagestyle{fancy} 
%   \fancyhead{}%
%   \fancyhead[LE,RO]{\headerFontSize\thepage}%
%   \fancyhead[RE]{\leftmark}%
%   \fancyhead[LO]{%
%     \iflanguage{\@defaultlanguage}%
%     {%
% %%      \headerFontSize\PFUheader
%      \rightmark
%     }
%     {%
%       \begin{otherlanguage*}{\@defaultlanguage}
% %%        \headerFontSize\PFUheader
%      \rightmark
%       \end{otherlanguage*}
%     }


% \renewcommand{\headrulewidth}{0pt}
% \renewcommand{\footrulewidth}{0pt}
% \fancyfoot[RO,LE]{{\small\textrm{\thepage}}}

% }

\def\@maketitle@hook@pre{\vspace{2\baselineskip plus \baselineskip
    minus \baselineskip}}

\renewcommand{\chapterFontShape}{\bfseries}

\renewcommand{\titleFontShape}{\bfseries}
\renewcommand{\titleFontSize}{\large}

\renewcommand{\sectionFontShape}{\bfseries}
\renewcommand{\sectionFontSize}{\normalfont}

\renewcommand{\subsectionFontShape}{\bfseries}
\renewcommand{\subsectionFontSize}{\normalfont}

\renewcommand{\paragraphFontShape}{\bfseries}

\renewcommand{\authorFontShape}{\bfseries}
\renewcommand{\authorFontSize}{\normalfont}

%{{{ \paperid{}

%\newwrite\paperidFile
%\immediate\openout\paperidFile=split-paper

%\renewcommand{\paperid}[1]{
%  \immediate\write\paperidFile{#1 \thepage}
%}

%\AtEndDocument{%
%  \immediate\closeout\paperidFile
%}

%\newwrite\trackidFile
%\immediate\openout\trackidFile=split-track

%\newcommand{\trackid}[1]{
%  \immediate\write\trackidFile{#1 \thepage}
%}

%\AtEndDocument{%
%  \immediate\closeout\trackidFile
%}

%}}}
