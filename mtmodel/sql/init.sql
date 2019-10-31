CREATE TABLE `c_lcs_game_comment_asp_count` (
  `source` varchar(255) NOT NULL COMMENT '游戏渠道',
  `game_id` varchar(255) NOT NULL COMMENT '游戏id',
  `game_name` varchar(255) NOT NULL COMMENT '游戏名',
  `aspects` text NOT NULL COMMENT '评论的标签',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`source`, `game_id`),
  KEY `game_name_key`(`game_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='c_lcs_game_comment_asp_count';

CREATE TABLE `c_lcs_game_comment_summary_base_asp` (
  `source` varchar(255) NOT NULL COMMENT '游戏渠道',
  `game_id` varchar(255) NOT NULL COMMENT '游戏id',
  `game_name` varchar(255) NOT NULL COMMENT '游戏名',
  `summaries` text NOT NULL COMMENT '摘要',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`source`, `game_id`),
  KEY `game_name_key`(`game_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='c_lcs_game_comment_summary_base_asp';

CREATE TABLE `c_game_comment_summary` (
  `source` varchar(255) NOT NULL COMMENT '游戏渠道',
  `game_id` varchar(255) NOT NULL COMMENT '游戏id',
  `game_name` varchar(255) NOT NULL COMMENT '游戏名',
  `summaries` text NOT NULL COMMENT '摘要',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`source`, `game_id`),
  KEY `game_name_key`(`game_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='c_game_comment_summary';


CREATE TABLE `c_game_ranking_by_bma_taptap` (
  `no` int(11) NOT NULL COMMENT '排名',
  `source` varchar(255) NOT NULL COMMENT '游戏渠道',
  `game_id` varchar(255) NOT NULL COMMENT '游戏id',
  `game_name` varchar(255) NOT NULL COMMENT '游戏名',
  `score` float NOT NULL COMMENT '游戏评分',
  `total` varchar(255) NOT NULL COMMENT '评分人数',
  `bma_score` float NOT NULL COMMENT '贝叶斯平均得分',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`no`),
  KEY `game_key`(`source`, `game_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='c_game_ranking_by_bma_taptap';

CREATE TABLE `c_game_ranking_by_wilson_taptap` (
  `no` int(11) NOT NULL COMMENT '排名',
  `source` varchar(255) NOT NULL COMMENT '游戏渠道',
  `game_id` varchar(255) NOT NULL COMMENT '游戏id',
  `game_name` varchar(255) NOT NULL COMMENT '游戏名',
  `score` float NOT NULL COMMENT '游戏评分',
  `total` varchar(255) NOT NULL COMMENT '评分人数',
  `wilson_score` float NOT NULL COMMENT '威尔逊评分',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`no`),
  KEY `game_key`(`source`, `game_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='c_game_ranking_by_wilson_taptap';

CREATE TABLE `c_game_ranking_by_weekly_wilson_score_taptap` (
  `no` int(11) NOT NULL COMMENT '排名',
  `source` varchar(255) NOT NULL COMMENT '游戏渠道',
  `game_id` varchar(255) NOT NULL COMMENT '游戏id',
  `game_name` varchar(255) NOT NULL COMMENT '游戏名',
  `score` float NOT NULL COMMENT '游戏评分',
  `total` float NOT NULL COMMENT '评分人数',
  `total_week` float NOT NULL COMMENT '一周之内平均得分',
  `wilson_score` float NOT NULL COMMENT '威尔逊评分',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`no`),
  KEY `game_key`(`source`, `game_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='c_game_ranking_by_wilson_score_taptap';

CREATE TABLE `c_game_ranking_by_weekly_comments_taptap` (
  `no` int(11) NOT NULL COMMENT '排名',
  `source` varchar(255) NOT NULL COMMENT '游戏渠道',
  `game_id` varchar(255) NOT NULL COMMENT '游戏id',
  `game_name` varchar(255) NOT NULL COMMENT '游戏名',
  `score` float NOT NULL COMMENT '游戏评分',
  `total` float NOT NULL COMMENT '评分人数',
  `total_week` float NOT NULL COMMENT '一周内增加评分人数',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`no`),
  KEY `game_key`(`source`, `game_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='c_game_ranking_by_weekly_comments_taptap';


