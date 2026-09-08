{assign var="unpadPublicUrl" value=$baseUrl|regex_replace:"~/ojs/?$~":""}
{if !$pageTitleTranslated}{capture assign="pageTitleTranslated"}{translate key=$pageTitle}{/capture}{/if}
{literal}<html lang="en-US" xml:lang="en-US"><head><style>body {transition: opacity ease-in 0.2s; } 
body[unresolved] {opacity: 0; display: block; overflow: hidden; position: relative; } 
</style>
	
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{/literal}{$pageTitleTranslated|escape}{literal} | Jurnal Bina Mulia Hukum</title>
	<meta name="generator" content="Peer Review Process | Jurnal Bina Mulia Hukum- Academic Pro ver 2.34 by openjournaltheme.com">	
	<meta name="robots" content="index follow">
	<meta name="googlebot" content="index follow">
				<meta name="description" content="">
	<meta name="og:description" content="">
	<meta name="author" content="Jurnal Bina Mulia Hukum">
	<meta name="copyright" content="Jurnal Bina Mulia Hukum">
			
<meta name="generator" content="Open Journal Systems 3.1.2.4">
<link rel="icon" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/c0380e34582a43a6d40a.png">

<meta name="ojtcontrolpanel" content="OJT Control Panel Version 2.0.6.3 by openjournaltheme.com">
	
	{/literal}{load_stylesheet context="frontend"}{literal}<link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/c16c57d4e947cafb58da.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/e2eb444fb48370818449.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/3d358f82b7cf770f1557.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/f2eee84cb465bd7173c4.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/1620f3323565dc019ba2.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/39656311ed9709c6b0f6.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/34575f574a718f532854.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/8fdd1d554686a88cd45e.css" type="text/css"><link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/vendor/73065faed541f3ce7dec.css" type="text/css">




<link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/assets/theme-compat.css">
<link rel="stylesheet" href="{/literal}{$unpadPublicUrl|escape}{literal}/ojs/plugins/themes/unpad/forms.css"></head>





<body class="pkp_page_peerreviewprocess pkp_op_index ">
	
		
	
	<div class="pkp_structure_page">

		<nav id="accessibility-nav" class="sr-only" role="navigation" aria-labelled-by="accessible-menu-label">
			<div id="accessible-menu-label">
				Quick jump to page content
			</div>
			<ul>
			  <li><a href="#main-navigation">Main Navigation</a></li>
			  <li><a href="#main-content">Main Content</a></li>
			  <li><a href="#sidebar">Sidebar</a></li>
			</ul>
		</nav>

				<header class="navbar navbar-default box-shadow background-white" id="headerNavigationContainer" role="banner">

						<div class="user_navigation">
			<div class="container">
				<div class="row">
									<button type="button" class="navbar-toggle collapsed pull-left" data-toggle="collapse" data-target="#nav-menu" aria-expanded="false" aria-controls="navbar">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<nav aria-label="User Navigation" class="pull-right">
						
				<ul id="navigationUser" class="nav nav-pills tab-list pull-right">
																					<li class="">
				<a href="{/literal}{$unpadPublicUrl|escape}{literal}/ojs/index.php/jbmh/login">
					Login
									</a>
							</li>
										</ul>
	
					</nav>
				</div><!-- .row -->
			</div><!-- .container-fluid -->
			</div>


			<div class="site_header">
			<div class="container">

				<div class="navbar-header  row display-flex">

					

																
						<h1 class="site-name ">
					
						
						
											
													<a href="{/literal}{$unpadPublicUrl|escape}{literal}/home.html" class="navbar-brand">Jurnal Bina Mulia Hukum</a>
																	</h1>
					
				</div>

								
									<nav id="nav-menu" class="navbar-collapse collapse" aria-label="Site Navigation">
																	
				<ul id="main-navigation" class="nav navbar-nav">
														<li class="">
				<a href="{/literal}{$unpadPublicUrl|escape}{literal}/home.html">
					Home
									</a>
							</li>
														<li class="">
				<a href="{/literal}{$unpadPublicUrl|escape}{literal}/issue/arcive.html">
					Archives
									</a>
							</li>
																												<li class=" dropdown">
				<a href="{/literal}{$unpadPublicUrl|escape}{literal}/About/about_journal.html" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
					About
											<span class="caret"></span>
									</a>
									<ul class="dropdown-menu ">
																					<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/About/about_journal.html">
										About the Journal
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/About/editorialTeam.html">
										Editorial Team
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/reviewers.html">
										Reviewers
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/peerreviewprocess.html">
										Peer Review Process
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/focus_scope.html">
										Focus and Scope
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/Open_access_policy.html">
										Open Access Policy
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/publication_ethics.html">
										Publication Ethics
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/about/privacy.html">
										Privacy Statement
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/copyrightnotice.html">
										Copyright Notice
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/plagiarism_check.html">
										Plagiarism Check
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/publication_frequency.html">
										Publication Frequency
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/indeks.html">
										Indeks
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/about/contact.html">
										Contact
									</a>
								</li>
																		</ul>
							</li>
																					<li class=" dropdown">
				<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/about/submissions.html" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
					Submissions
											<span class="caret"></span>
									</a>
									<ul class="dropdown-menu ">
																					<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/ojs/index.php/jbmh/submission">
										online_submissions
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/authorguidelines.html">
										Author Guidelines
									</a>
								</li>
																												<li class="">
									<a href="https://docs.google.com/document/d/1LBbIFAnLkw-zlAX_xOYcdYz37_zf-Oz8/edit?usp=sharing&amp;ouid=103161228605528742071&amp;rtpof=true&amp;sd=true">
										Manuscript Template
									</a>
								</li>
																												<li class="">
									<a href="{/literal}{$unpadPublicUrl|escape}{literal}/pages/fees.html">
										Fees
									</a>
								</li>
																		</ul>
							</li>
			</ul>
	
				

																			<div class="pull-md-right search_input">
								
 <a href="{/literal}{$unpadPublicUrl|escape}{literal}/search.html"> <button type="submit" class="btn btn-default"><i class="fa fa-search"> </i> Search</button> </a>

							</div>
											</nav>
				
			</div><!-- .pkp_head_wrapper -->

			</div>


			<div class="header_shadow"></div>


		</header><!-- .pkp_structure_head -->



		<div class="row journal_index header_section">


			<div class="container journal_name_logo ">
				<div class="col-md-5 site_logo">
				
					
														</div>	
				
				
			</div>	



							<div class="container journal_name_logo ">
					<div class="col-md-12 about_journal">
						<h1>{/literal}{$pageTitleTranslated|escape}{literal}</h1>
						<p>
						
						</p>
					</div>
				</div>
			


		</div>	
		<div class="pkp_structure_content container main_content">
			<main class="pkp_structure_main col-xs-12 col-sm-7   col-md-8  " role="main" id="pkp_content_main">

		




		
{/literal}